"""Phase 2 — Inclusion filter.

Filter the raw AIID snapshot to the analysis window (2023-01-01 .. 2026-06-30)
and apply the three inclusion criteria. Emits:
  - data/filtered/in_scope.csv   (candidates to be hand-coded)
  - data/filtered/excluded.csv   (incident_id, reason)

Inclusion (all must hold): deployed conversational/agentic system interacting
with end users; harm from the system's output/action in an interaction; enough
public detail to see the triggering input. See METHODOLOGY.md.

STUB: window + date parsing wired; criteria are judgement calls seeded from the
raw fields, then confirmed during coding.
"""
from __future__ import annotations

from pathlib import Path

WINDOW_START = "2023-01-01"
WINDOW_END = "2026-06-30"

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "filtered"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # TODO(phase2): load latest snapshot from RAW_DIR, restrict to
    #   WINDOW_START..WINDOW_END on year-of-first-report, apply the three
    #   inclusion criteria, and write in_scope.csv / excluded.csv.
    raise SystemExit("filter_incidents: implement once the raw snapshot exists.")


if __name__ == "__main__":
    main()
