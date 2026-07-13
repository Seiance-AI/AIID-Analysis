# AIID Triggering-Input Analysis — Results Report

**Window:** 2023-01-01 → 2026-06-30 (year basis: AIID incident date) ·
**Export accessed:** 2026-07-07 · **Computed:** 2026-07-13

## Headline numbers (the `[■]` placeholders)

| Placeholder | Value |
|---|---|
| `[■ N]` total in-scope incidents | **199** |
| `[■ X]%` normative share, X = C/N (purist, as locked) | **83.9%** |
| (B+C)/N, the broader "no adversarial technique" number | 90.5% |
| `[■ A]% → [■ B]%` A-share, 2023 → 2025 | **12.5% → 13.3%** |
| `[■ C]% → [■ D]%` C-share, 2023 → 2025 | **81.2% → 79.6%** |

## Category counts by year

| Year | A (Adversarial) | B (Social pressure) | C (Normative) | Total | C-share |
|---|---|---|---|---|---|
| 2023 | 4 | 2 | 26 | 32 | 81.2% |
| 2024 | 1 | 1 | 39 | 41 | 95.1% |
| 2025 | 13 | 7 | 78 | 98 | 79.6% |
| 2026 (H1) | 1 | 3 | 24 | 28 | 85.7% |
| **All** | **19** | **13** | **167** | **199** | **83.9%** |

## ⚠️ Honesty check (Part 4 of the rubric): trend claim FAILS

Adversarial share did **not** fall between the first and last full year
(12.5% → 13.3%; the 2024 dip to 2.4% makes the series non-monotonic and the
per-year A counts are small: 4, 1, 13, 1). Per the pre-registered rule:
**do not claim a falling adversarial share from AIID data.** Frame Chart 1 as
the composition claim — *"the overwhelming majority (~84%) of real-world
conversational/agentic AI incidents are triggered by ordinary, good-faith
use, not attacks"* — which holds in every year (79.6–95.1%). Let provider
data (Chart 2) carry any "adversarial is being solved upstream" trend alone.

## Optional stat: enforceable vs reputational harm

- **C (normative): 37.1%** involved legal, financial, or regulatory
  consequences (62 of 167)
- A (adversarial): 42.1% (8 of 19) — small n, dominated by agentic-exploit
  cases with financial loss
- B (social pressure): 15.4% (2 of 13)

Usable phrasing: "normative incidents carried enforceable consequences at more
than double the rate of social-pressure incidents (37% vs 15%)." (The A rate is
not lower than C's, so avoid the C-vs-A framing the spec sketched.)

## Methodology stats (for the note)

- Pipeline: 1,032 window incidents → keyword triage (242 candidates + 17
  ambiguous coded; 519 excluded) → recall screen of the 254 no-keyword-match
  rows promoted 78 more → **337 incidents fully coded** → N=199 in scope.
- Exclusions: **833** total (triage 519, screen 176, coding 138), each with a
  one-word reason in `data/filtered/exclusions_full.csv`.
- Coding: dual-coded by two independent LLM passes with identical rubric
  prompts (336/337 dual-coded); scope agreement **91.7%**, category agreement
  **96.4%**; 56 disagreements resolved by a third independent adjudication
  pass with per-incident notes.

## Deliverable files

- `coding/coded_incidents.csv` — the coding sheet: 199 in-scope incidents with
  year, system_type, one-line description, harm_type, both coders' categories,
  final category, and disagreement notes.
- `output/counts/counts_by_year.csv` — A/B/C counts and shares per year.
- `output/counts/summary.json` — every number above, machine-readable.
- `coding/coding_audit.csv` — all 337 coded incidents incl. the 138 coded-out.
- `coding/raw_codings/` — raw per-coder JSON (the dual-coding evidence).
