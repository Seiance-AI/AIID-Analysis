"""Phase 1 — Data ingest / provenance.

The AIID full export was provided as an Excel snapshot rather than pulled live,
so this script verifies the snapshot is present in data/raw/ and records the
access date (the export's own generation date, read from its README sheet).

Snapshot: data/raw/AI_Incident_Database_Full_Export.xlsx
  - generated 2026-07-07 via AIID's public read-only GraphQL API
  - sheets: README, Incidents (1560), Reports (7300), Entities (5222)

Usage:
    python scripts/pull_data.py
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
SNAPSHOT = RAW_DIR / "AI_Incident_Database_Full_Export.xlsx"


def main() -> None:
    if not SNAPSHOT.exists():
        raise SystemExit(
            f"Snapshot not found at {SNAPSHOT}. Place the AIID export there first."
        )
    readme = pd.read_excel(SNAPSHOT, sheet_name="README", header=None)
    text = "\n".join(str(v) for v in readme.iloc[:, 0].tolist())
    m = re.search(r"Generated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    access_date = m.group(1) if m else "unknown"
    (RAW_DIR / "ACCESS_DATE.txt").write_text(access_date + "\n")

    counts = {
        s: pd.read_excel(SNAPSHOT, sheet_name=s).shape[0]
        for s in ("Incidents", "Reports", "Entities")
    }
    print(f"Snapshot OK: {SNAPSHOT.name}")
    print(f"Access date (export generated): {access_date}")
    for s, n in counts.items():
        print(f"  {s}: {n} rows")


if __name__ == "__main__":
    main()
