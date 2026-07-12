"""Phase 3 assembly — merge dual-coder results into the final coding sheet.

Reads raw coding outputs from coding/raw_codings/:
  <batch>_c1.json / <batch>_c2.json   {"codings": [...]} per independent coder
  <batch>_screen.json                 {"flagged": [...]} recall-screen results
  adj_*.json                          {"decisions": [...]} adjudications

Resolution rules (mirrors METHODOLOGY.md):
  - Both coders agree on scope + category (+ system_type/harm_type when in
    scope): coder1's coding is final; exclusion_reason prefers the more
    specific "out-of-scope-type" if either coder chose it.
  - Any mismatch on scope/category/system_type/harm_type: requires an
    adjudication decision. If none exists yet the incident is listed as a
    pending dispute and the script exits nonzero (run adjudication, rerun).
  - Only one coder produced a coding: it is final, noted "single-coded".

Outputs:
  coding/coded_incidents.csv      in-scope incidents only (the coding sheet)
  coding/coding_audit.csv         every coded incident, both coder verdicts
  data/filtered/exclusions_full.csv  full exclusion audit (triage+screen+coding)
  coding/pending_disputes.json    written only when adjudication is incomplete

Usage: python scripts/assemble_coding.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "coding" / "raw_codings"
FILTERED = ROOT / "data" / "filtered"

CATS = {"A", "B", "C"}


def load_maps():
    c1, c2, adj, screens = {}, {}, {}, {}
    for f in sorted(RAW.glob("*.json")):
        data = json.loads(f.read_text())
        if f.name.endswith("_c1.json"):
            for c in data["codings"]:
                c1[c["incident_id"]] = c
        elif f.name.endswith("_c2.json"):
            for c in data["codings"]:
                c2[c["incident_id"]] = c
        elif f.name.startswith("adj_"):
            for d in data["decisions"]:
                adj[d["incident_id"]] = d
        elif f.name.endswith("_screen.json"):
            screens[f.name.replace("_screen.json", "")] = data["flagged"]
    return c1, c2, adj, screens


def needs_adjudication(a, b):
    if a["in_scope"] != b["in_scope"]:
        return "scope"
    if a["in_scope"]:
        if a["category"] != b["category"]:
            return "category"
        if a["system_type"] != b["system_type"] or a["harm_type"] != b["harm_type"]:
            return "fields"
    return None


def main() -> None:
    cand = list(csv.DictReader((FILTERED / "in_scope_candidates.csv").open()))
    review = list(csv.DictReader((FILTERED / "review_queue.csv").open()))
    triage_excluded = list(csv.DictReader((FILTERED / "excluded.csv").open()))

    meta = {}
    for r in cand:
        meta[int(r["incident_id"])] = {"year": r["year"], "title": r["title"], "bucket": "candidate"}
    for r in review:
        b = "ambiguous" if r["reason"] == "ambiguous-both-signals" else "review"
        meta[int(r["incident_id"])] = {"year": r["year"], "title": r["title"], "bucket": b}

    c1, c2, adj, screens = load_maps()
    flagged_ids = {f["incident_id"] for fl in screens.values() for f in fl}
    coded_ids = sorted(set(c1) | set(c2))

    disputes, audit_rows = [], []
    for iid in coded_ids:
        a, b = c1.get(iid), c2.get(iid)
        m = meta.get(iid, {"year": "", "title": "", "bucket": "?"})
        bucket = "promoted" if m["bucket"] == "review" else m["bucket"]
        adjudicated, note = False, ""
        if a and b:
            why = needs_adjudication(a, b)
            if why:
                if iid in adj:
                    fin, adjudicated = adj[iid], True
                    note = fin.get("note", "") or f"adjudicated ({why})"
                else:
                    disputes.append({"incident_id": iid, "why": why, "coder1": a, "coder2": b})
                    continue
            else:
                fin = dict(a)
                if not a["in_scope"] and (
                    a["exclusion_reason"] == "out-of-scope-type"
                    or b["exclusion_reason"] == "out-of-scope-type"
                ):
                    fin["exclusion_reason"] = "out-of-scope-type"
        else:
            fin = a or b
            note = "single-coded: one coder pass failed"

        audit_rows.append({
            "incident_id": iid,
            "year": m["year"],
            "bucket": bucket,
            "coder1_in_scope": a["in_scope"] if a else "",
            "coder1_category": (a["category"] if a else ""),
            "coder2_in_scope": b["in_scope"] if b else "",
            "coder2_category": (b["category"] if b else ""),
            "adjudicated": adjudicated,
            "final_in_scope": fin["in_scope"],
            "final_category": fin["category"],
            "exclusion_reason": "n/a" if fin["in_scope"] else fin["exclusion_reason"],
            "system_type": fin["system_type"],
            "harm_type": fin["harm_type"],
            "description": fin["one_line"],
            "disagreement_note": note,
        })

    if disputes:
        out = ROOT / "coding" / "pending_disputes.json"
        out.write_text(json.dumps(disputes, indent=1))
        print(f"{len(disputes)} disputes need adjudication -> {out}")
        sys.exit(1)

    (ROOT / "coding").mkdir(exist_ok=True)
    with (ROOT / "coding" / "coding_audit.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(audit_rows[0].keys()))
        w.writeheader()
        w.writerows(audit_rows)

    sheet_cols = ["incident_id", "year", "system_type", "description", "harm_type",
                  "coder1_category", "coder2_category", "final_category", "disagreement_note"]
    with (ROOT / "coding" / "coded_incidents.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=sheet_cols)
        w.writeheader()
        for r in audit_rows:
            if r["final_in_scope"] is True:
                w.writerow({k: r[k] for k in sheet_cols})

    # Full exclusion audit: keyword triage + screen-cleared + coded-out.
    excl_rows = [{"incident_id": r["incident_id"], "year": r["year"],
                  "stage": "keyword-triage", "reason": "out-of-scope-type"}
                 for r in triage_excluded]
    for r in review:
        iid = int(r["incident_id"])
        if meta[iid]["bucket"] == "review" and iid not in flagged_ids:
            excl_rows.append({"incident_id": iid, "year": r["year"],
                              "stage": "recall-screen", "reason": "out-of-scope-type"})
    for r in audit_rows:
        if r["final_in_scope"] is not True:
            excl_rows.append({"incident_id": r["incident_id"], "year": r["year"],
                              "stage": "coding", "reason": r["exclusion_reason"]})
    with (FILTERED / "exclusions_full.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["incident_id", "year", "stage", "reason"])
        w.writeheader()
        w.writerows(excl_rows)

    n_in = sum(1 for r in audit_rows if r["final_in_scope"] is True)
    both = [r for r in audit_rows if r["coder1_in_scope"] != "" and r["coder2_in_scope"] != ""]
    scope_agree = sum(1 for r in both if r["coder1_in_scope"] == r["coder2_in_scope"])
    cat_pool = [r for r in both if r["coder1_in_scope"] is True and r["coder2_in_scope"] is True]
    cat_agree = sum(1 for r in cat_pool if r["coder1_category"] == r["coder2_category"])
    print(f"coded={len(audit_rows)} in_scope N={n_in} "
          f"| dual-coded={len(both)} scope-agree={scope_agree}/{len(both)} "
          f"category-agree={cat_agree}/{len(cat_pool)} "
          f"| adjudicated={sum(1 for r in audit_rows if r['adjudicated'])} "
          f"| exclusions={len(excl_rows)}")
    print("wrote coding/coded_incidents.csv, coding/coding_audit.csv, data/filtered/exclusions_full.csv")


if __name__ == "__main__":
    main()
