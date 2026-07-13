# Methodology — AIID Triggering-Input Analysis

This file is the running methodology note and the coding rubric ("rubric
available on request"). It records the fixed parameters of the analysis and the
rules used to code each incident. Fill in the bracketed values as the work
progresses.

## Fixed parameters (locked)

| Parameter            | Value                                                        |
|----------------------|--------------------------------------------------------------|
| Data source          | AI Incident Database export (incidentdatabase.ai)            |
| Access date          | 2026-07-07 (export generated via AIID public GraphQL API)     |
| Analysis window      | 2023-01-01 → 2026-06-30 (Q2 2026, most recent complete qtr)  |
| Year basis           | AIID incident `date` field (incident-occurrence date)        |
| Year buckets         | 2023, 2024, 2025 (full) + 2026 (partial)                     |
| First vs last full year | 2023 vs 2025                                              |
| Coding               | Dual-coded; disagreements resolved by discussion             |
| `X%` definition      | Purist: `C / N` ("ordinary use, no manipulation at all")     |
| Deliverable          | Coded CSV + per-category-per-year counts (no chart render)   |

**Note on year basis.** Year buckets are taken from the AIID `date` field
(the incident-occurrence date) rather than the earliest linked report date.
The two agree on the year for ~82% of incidents; the incident date is used for
simplicity and because it is the field AIID surfaces directly. Charts and
counts should describe the axis as "year (AIID incident date)".

## Part 2 — Inclusion criteria

An incident is **in scope** only if ALL hold:

1. Involves a **deployed conversational or agentic AI system** interacting with
   end users (chatbot, voice agent, support agent, copilot, autonomous agent).
2. The harm arises from the **system's output or action in an interaction** —
   not training-data disputes, third-party deepfakes, facial recognition,
   recommender systems, or autonomous vehicles.
3. Enough public documentation to determine **what the triggering input looked
   like**.

Log each exclusion with a one-word reason: `out-of-scope-type` or
`insufficient-detail`. Exclusion count: **833** (keyword triage 519,
recall screen 176, coding 138; see `data/filtered/exclusions_full.csv`).

## Part 3 — Coding categories

Code by the **nature of the triggering input**, not the severity of the outcome.

- **A — Adversarial.** A deliberate technical exploit was required: prompt
  injection (direct/indirect), jailbreak templates, roleplay coercion to bypass
  safety, encoding/obfuscation (Base64, leetspeak, token smuggling), adversarial
  suffixes, poisoned documents/tools.
  *Test: would an input filter or safety classifier plausibly have had something
  anomalous to catch?* Yes → A.
- **B — Social pressure.** No technical exploit, but the user was deliberately
  manipulating, goading, or toying with the system to make it misbehave (for
  fun, screenshots, or advantage). *Test: was the user's goal to make the system
  fail, with no technical exploit?* Yes → B.
- **C — Normative.** Ordinary use by an ordinary user, in plain language, in
  good faith, consistent with the system's intended purpose — and it failed
  anyway. *Test: would this input pass unnoticed in a random sample of
  legitimate traffic?* Yes → C.

### Tie-breakers
- Persistence alone (repeating, urgency, emotion) is **not** social pressure —
  real customers do this. Stays in C.
- If an incident began normatively and the user later escalated into
  manipulation, code by the input that produced the harmful output.
- On coder disagreement: second coder reviews independently; resolve by
  discussion.

## Part 4 — Numbers to produce

- `N` = total in-scope incidents.
- `X% = C / N` — ordinary use with no adversarial technique whatsoever.
- A-share: 2023 vs 2025.
- C-share: 2023 vs 2025.
- Optional: enforceable/regulatory-harm share of C vs of A.

**Honesty check:** if adversarial share does not fall across years, do not force
the claim — report the composition finding ("most real incidents are
normative") instead.

## Coding process (as executed)

The 1,032 window incidents were triaged by a transparent keyword funnel into
242 candidates, 519 clear exclusions, and 271 for review. The 242 candidates
plus 17 keyword-ambiguous incidents were fully coded; the remaining 254
no-keyword-match incidents went through a recall-oriented screen (erring toward
inclusion), which promoted 78 for full coding — 337 incidents coded in total.

Coding was **model-assisted and dual-coded**: two independent LLM coding passes
using identical rubric prompts, coding strictly from AIID incident material
(title, description, and linked report text; no web access, no outside
knowledge). Disagreements on scope, category, or fields were resolved by a
third independent adjudication pass reviewing both codings and the source
material; adjudication notes are recorded per incident. Raw per-coder outputs
live in `coding/raw_codings/`.

- Dual-coded: 336 of 337 (one incident single-coded after a coder-pass fault)
- Scope agreement: **91.7%**; category agreement (both-in-scope pool of 196): **96.4%**
- Adjudicated: 56 incidents

## Results (computed 2026-07-13)

- **N = 199** in-scope incidents: **A = 19, B = 13, C = 167**
- **X% = C/N = 83.9%** (purist); (B+C)/N = 90.5%
- A-share 2023 → 2025: **12.5% → 13.3%**; C-share: **81.2% → 79.6%**
- Enforceable-harm share: C 37.1%, A 42.1%, B 15.4%
- **Honesty check: adversarial share is NOT falling** (12.5% → 13.3%).
  Per Part 4, Chart 1 must be framed as a composition claim ("the overwhelming
  majority of real-world conversational/agentic AI incidents are normative"),
  and any "adversarial is being solved upstream" trend must be carried by
  provider data (Chart 2) alone.
