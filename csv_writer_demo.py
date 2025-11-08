from datetime import datetime, timezone
import csv
from pathlib import Path

ROWS = [
    {"id": 1, "name": "Alpha"},
    {"id": 2, "name": "Beta"},
    {"id": 3, "name": "Gamma"},
]

def main():
    for r in ROWS:
        r["ts"] = datetime.now(timezone.utc).isoformat()

    out = Path("sample_data.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "ts"])
        w.writeheader()
        w.writerows(ROWS)

    print(f"Wrote {out.resolve()} with {len(ROWS)} rows")

if __name__ == "__main__":
    main()
