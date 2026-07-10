# AIID-Analysis

Analysis of the AI Incident Database (AIID): coding deployed
conversational/agentic AI incidents by **triggering-input type** (Adversarial /
Social pressure / Normative) and producing the counts behind an article's
figures.

Deliverable: a **coded CSV + per-category-per-year counts** (charts produced
downstream in the article's style).

## Parameters (locked)

- Window: **2023-01-01 → 2026-06-30** (Q2 2026, most recent complete quarter)
- Coding: **dual-coded**, disagreements resolved by discussion
- Headline stat: **`X% = C / N`** (purist — ordinary use, no manipulation)
- Python **3.12**

## Layout

```
data/raw/         AIID export snapshot (git-ignored; archive out-of-band)
data/filtered/    in_scope.csv + excluded.csv (with reasons)
coding/           dual-coding sheet template + column spec
scripts/          pull_data → filter_incidents → compute_counts
output/counts/    counts_by_year.csv + summary.json (final deliverable)
METHODOLOGY.md    fixed parameters + full A/B/C rubric & tie-breakers
```

## Workflow

1. **Pull** — `python scripts/pull_data.py` (records access date)
2. **Filter** — `python scripts/filter_incidents.py` (window + inclusion criteria)
3. **Code** — hand-code `in_scope.csv` into `coding/` per `METHODOLOGY.md`
4. **Compute** — `python scripts/compute_counts.py` (N, X%=C/N, year shares)

## Setup

```
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
