"""Phase 1 — Data pull.

Download the full AI Incident Database export and record the access date.

STUB: fill in the export URL/format once confirmed on incidentdatabase.ai.
Writes the raw snapshot to data/raw/ and stamps the access date into a sidecar
file so it can be copied into METHODOLOGY.md.

Usage:
    python scripts/pull_data.py
"""
from __future__ import annotations

from datetime import date, timezone, datetime
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# TODO(phase1): confirm the current export endpoint/format on incidentdatabase.ai
#   (Research/download section provides CSV/JSON snapshots).
EXPORT_URL = None


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    access = datetime.now(timezone.utc).date().isoformat()
    (RAW_DIR / "ACCESS_DATE.txt").write_text(access + "\n")
    if EXPORT_URL is None:
        raise SystemExit(
            "EXPORT_URL not set — confirm the AIID export location, then fill it in."
        )
    # TODO(phase1): stream EXPORT_URL to data/raw/ and verify integrity.


if __name__ == "__main__":
    main()
