# Coding sheet

`coding_sheet_template.csv` is the dual-coding worksheet. One row per **in-scope**
incident. Columns:

| Column               | Values / notes                                                        |
|----------------------|-----------------------------------------------------------------------|
| `incident_id`        | AIID incident ID                                                      |
| `year_first_report`  | Year of first report (2023–2026)                                     |
| `system_type`        | `customer service` \| `gov info` \| `dev tool` \| `other`            |
| `description`        | One-line description                                                  |
| `harm_type`          | `enforceable` (legal/financial/regulatory) \| `reputational`         |
| `coder1_category`    | `A` \| `B` \| `C`                                                    |
| `coder2_category`    | `A` \| `B` \| `C`                                                    |
| `final_category`     | `A` \| `B` \| `C` (after resolving disagreements by discussion)      |
| `disagreement_note`  | Left blank unless coders disagreed; note how it was resolved         |

Excluded incidents do **not** go here — they go in `data/filtered/excluded.csv`
with a one-word reason (`out-of-scope-type` / `insufficient-detail`).

See `../METHODOLOGY.md` for the full A/B/C rubric and tie-breakers.
