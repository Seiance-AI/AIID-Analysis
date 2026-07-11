"""Phase 2 — Window filter + inclusion triage.

Restricts the AIID Incidents snapshot to the analysis window and triages each
incident with a transparent keyword funnel into three buckets:

  in_scope_candidates.csv  keyword-plausible deployed conversational/agentic
                           incidents -> the primary HAND-CODING queue
  excluded.csv             clearly out-of-scope types (deepfakes, AVs, facial
                           recognition, etc.) -> reason=out-of-scope-type
  review_queue.csv         ambiguous (both signals) or no-keyword-match ->
                           lighter second-pass human review (nothing is
                           silently dropped)

The keyword funnel is a RECALL AID, not the coding decision. Final in/out and
A/B/C classification are made by humans per METHODOLOGY.md against the article's
uploaded snapshot. Year is taken from the AIID incident `date` field.

Usage:
    python scripts/filter_incidents.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

WINDOW_START = pd.Timestamp("2023-01-01")
WINDOW_END = pd.Timestamp("2026-06-30")

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "raw" / "AI_Incident_Database_Full_Export.xlsx"
OUT_DIR = ROOT / "data" / "filtered"

# Signals that an incident MAY involve a deployed conversational/agentic system
# interacting with end users. (Editable — kept transparent for defensibility.)
IN_SIGNALS = [
    "chatbot", "chat bot", "conversational", "virtual assistant", "ai assistant",
    "customer service bot", "customer service agent", "support bot", "support agent",
    "copilot", "voice assistant", "voice agent", "ai agent", "agentic",
    "large language model", " llm", "chatgpt", "gemini", "claude", "grok",
    "bard", "replika", "character.ai", "character ai", "helpline", "help desk bot",
    "told the user", "advised the user", "responded to the user", "gave advice",
    "generated a response", "coding assistant", "code assistant", "cursor",
]

# Signals of the AIID-dominant OUT-OF-SCOPE incident types.
OUT_SIGNALS = [
    "deepfake", "deep fake", "synthetic media", "synthetic video", "synthetic audio",
    "voice clone", "voice-clone", "cloned voice", "face swap", "face-swap",
    "facial recognition", "face recognition", "self-driving", "driver-assist",
    "driver assistance", "autopilot", "autonomous vehicle", "autonomous driving",
    "robotaxi", "recommender system", "recommendation algorithm",
    "non-consensual", "nonconsensual", "nudify", "csam", "child sexual",
    "predictive policing", "image generator", "image-generation",
]


def contains_any(series: pd.Series, needles: list[str]) -> pd.Series:
    pat = "|".join(pd.Series(needles).str.replace(r"([.^$*+?()\[\]{}|\\])", r"\\\1", regex=True))
    return series.str.contains(pat, regex=True, na=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inc = pd.read_excel(SNAPSHOT, sheet_name="Incidents")
    inc["date"] = pd.to_datetime(inc["date"], errors="coerce")

    win = inc[(inc["date"] >= WINDOW_START) & (inc["date"] <= WINDOW_END)].copy()
    win["year"] = win["date"].dt.year

    blob = (
        win["title"].fillna("") + " "
        + win["description"].fillna("") + " "
        + win["deployers"].fillna("") + " "
        + win["developers"].fillna("")
    ).str.lower()
    win["in_signal"] = contains_any(blob, IN_SIGNALS)
    win["out_signal"] = contains_any(blob, OUT_SIGNALS)

    is_candidate = win["in_signal"] & ~win["out_signal"]
    is_excluded = win["out_signal"] & ~win["in_signal"]
    is_review = ~is_candidate & ~is_excluded  # both-signals or no-keyword-match

    ref_cols = ["incident_id", "year", "title", "description", "incident_url"]

    # Hand-coding queue: reference columns + blank coding columns to fill in.
    coding_cols = [
        "system_type", "harm_type",
        "coder1_category", "coder2_category", "final_category", "disagreement_note",
    ]
    cand = win[is_candidate][ref_cols].copy()
    for c in coding_cols:
        cand[c] = ""
    cand.sort_values("date" if "date" in cand else "incident_id")
    cand.to_csv(OUT_DIR / "in_scope_candidates.csv", index=False)

    excl = win[is_excluded][["incident_id", "year", "title"]].copy()
    excl["reason"] = "out-of-scope-type"
    excl.to_csv(OUT_DIR / "excluded.csv", index=False)

    review = win[is_review][ref_cols + ["in_signal", "out_signal"]].copy()
    review["reason"] = review.apply(
        lambda r: "ambiguous-both-signals" if r["in_signal"] else "no-keyword-match",
        axis=1,
    )
    review.to_csv(OUT_DIR / "review_queue.csv", index=False)

    # Full window audit trail.
    win[ref_cols + ["in_signal", "out_signal"]].to_csv(
        OUT_DIR / "in_window.csv", index=False
    )

    print(f"Window {WINDOW_START.date()}..{WINDOW_END.date()}: {len(win)} incidents")
    print(f"  in_scope_candidates : {is_candidate.sum():>4}  -> hand-code these")
    print(f"  excluded            : {is_excluded.sum():>4}  (out-of-scope-type)")
    print(f"  review_queue        : {is_review.sum():>4}  (ambiguous / no-keyword-match)")
    print("Wrote in_scope_candidates.csv, excluded.csv, review_queue.csv, in_window.csv")


if __name__ == "__main__":
    main()
