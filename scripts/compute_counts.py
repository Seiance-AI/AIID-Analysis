"""Phase 4 — Compute the numbers.

Read the completed dual-coding sheet (final_category populated) and emit the
counts that fill the article placeholders. Deliverable is CSV + counts only.

Outputs (to output/counts/):
  - counts_by_year.csv        A/B/C counts and shares per year
  - summary.json              N, X% = C/N, A-share & C-share for 2023 vs 2025,
                              and the enforceable-vs-reputational harm split

Definitions (locked):
  N   = total in-scope incidents
  X%  = C / N               (purist: ordinary use, no manipulation at all)
  A-share / C-share compared for first vs last full year: 2023 vs 2025

STUB: implement once coding is complete.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODING = ROOT / "coding"
OUT = ROOT / "output" / "counts"

FIRST_FULL_YEAR = 2023
LAST_FULL_YEAR = 2025


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # TODO(phase4): load the completed coding sheet, group by year & category,
    #   compute N, X% = C/N, A/C shares for 2023 vs 2025, and the enforceable
    #   harm split; run the honesty check before finalizing Chart 1 framing.
    raise SystemExit("compute_counts: implement once the coding sheet is filled.")


if __name__ == "__main__":
    main()
