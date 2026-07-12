"""Phase 4 — Compute the numbers that fill the article placeholders.

Reads coding/coded_incidents.csv (in-scope, final_category populated) and
coding/coding_audit.csv / data/filtered/exclusions_full.csv for the
methodology stats.

Outputs (output/counts/):
  counts_by_year.csv   A/B/C counts and shares per year
  summary.json         N, X% = C/N, A-share & C-share 2023 vs 2025,
                       enforceable-harm split, agreement stats, exclusions

Definitions (locked): N = total in-scope; X% = C/N (purist);
first vs last full year = 2023 vs 2025; year basis = AIID incident date.
Includes the Part 4 honesty check on the adversarial-share trend.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "counts"
FIRST_FULL_YEAR, LAST_FULL_YEAR = 2023, 2025


def share(part: int, whole: int) -> float:
    return round(100.0 * part / whole, 1) if whole else 0.0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader((ROOT / "coding" / "coded_incidents.csv").open()))
    for r in rows:
        r["year"] = int(r["year"])

    years = sorted({r["year"] for r in rows})
    by_year = []
    for y in years:
        yr = [r for r in rows if r["year"] == y]
        a = sum(1 for r in yr if r["final_category"] == "A")
        b = sum(1 for r in yr if r["final_category"] == "B")
        c = sum(1 for r in yr if r["final_category"] == "C")
        t = len(yr)
        by_year.append({"year": y, "A": a, "B": b, "C": c, "total": t,
                        "a_share_pct": share(a, t), "b_share_pct": share(b, t),
                        "c_share_pct": share(c, t)})
    with (OUT / "counts_by_year.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(by_year[0].keys()))
        w.writeheader()
        w.writerows(by_year)

    n = len(rows)
    cat = {k: sum(1 for r in rows if r["final_category"] == k) for k in "ABC"}
    yr_first = next((d for d in by_year if d["year"] == FIRST_FULL_YEAR), None)
    yr_last = next((d for d in by_year if d["year"] == LAST_FULL_YEAR), None)

    def harm_split(category: str) -> dict:
        pool = [r for r in rows if r["final_category"] == category]
        enf = sum(1 for r in pool if r["harm_type"] == "enforceable")
        return {"n": len(pool), "enforceable": enf,
                "enforceable_pct": share(enf, len(pool))}

    audit = list(csv.DictReader((ROOT / "coding" / "coding_audit.csv").open()))
    both = [r for r in audit if r["coder1_in_scope"] and r["coder2_in_scope"]]
    scope_agree = sum(1 for r in both if r["coder1_in_scope"] == r["coder2_in_scope"])
    cat_pool = [r for r in both
                if r["coder1_in_scope"] == "True" and r["coder2_in_scope"] == "True"]
    cat_agree = sum(1 for r in cat_pool if r["coder1_category"] == r["coder2_category"])

    excl = list(csv.DictReader((ROOT / "data" / "filtered" / "exclusions_full.csv").open()))
    excl_by_stage: dict[str, int] = {}
    for r in excl:
        excl_by_stage[r["stage"]] = excl_by_stage.get(r["stage"], 0) + 1

    summary = {
        "window": "2023-01-01..2026-06-30",
        "year_basis": "AIID incident date",
        "access_date": "2026-07-07",
        "N_in_scope": n,
        "counts": cat,
        "X_pct_C_over_N": share(cat["C"], n),
        "BC_pct_over_N": share(cat["B"] + cat["C"], n),
        "A_share_first_vs_last_full_year": {
            str(FIRST_FULL_YEAR): yr_first["a_share_pct"] if yr_first else None,
            str(LAST_FULL_YEAR): yr_last["a_share_pct"] if yr_last else None,
        },
        "C_share_first_vs_last_full_year": {
            str(FIRST_FULL_YEAR): yr_first["c_share_pct"] if yr_first else None,
            str(LAST_FULL_YEAR): yr_last["c_share_pct"] if yr_last else None,
        },
        "enforceable_harm_split": {k: harm_split(k) for k in "ABC"},
        "coder_agreement": {
            "dual_coded": len(both),
            "scope_agreement_pct": share(scope_agree, len(both)),
            "category_agreement_pct": share(cat_agree, len(cat_pool)),
            "category_agreement_pool": len(cat_pool),
        },
        "exclusions": {"total": len(excl), "by_stage": excl_by_stage},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(json.dumps(summary, indent=2))
    if yr_first and yr_last:
        falling = yr_last["a_share_pct"] < yr_first["a_share_pct"]
        print(f"\nHONESTY CHECK: adversarial share {yr_first['a_share_pct']}% (2023) -> "
              f"{yr_last['a_share_pct']}% (2025): "
              + ("falling — trend claim OK." if falling else
                 "NOT falling — reframe Chart 1 as a composition claim."))


if __name__ == "__main__":
    main()
