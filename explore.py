import time
from pathlib import Path

import pandas as pd
from ckanapi import RemoteCKAN

PORTAL_URL = "https://data.gov.au/data/"
RESOURCE_ID = "591cb009-1167-4008-b7e8-f5fc9dbbb511"
RAW_DIR = Path("data/raw")
PAGE_SIZE = 5000


def extract_placements(max_rows=None):
    """Page through the CKAN datastore table and save the raw rows to CSV."""
    rc = RemoteCKAN(PORTAL_URL)
    rows = []
    offset = 0

    while True:
        result = rc.action.datastore_search(
            resource_id=RESOURCE_ID,
            limit=PAGE_SIZE,
            offset=offset,
        )
        records = result["records"]
        if not records:
            break

        rows.extend(records)
        offset += len(records)
        print(f"Fetched {len(rows)} of {result['total']} rows")

        if max_rows and len(rows) >= max_rows:
            rows = rows[:max_rows]
            break

        time.sleep(0.5)  # be polite to the server

    df = pd.DataFrame(rows)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "job_placements_raw.csv"
    df.to_csv(raw_path, index=False)
    print(f"Saved {len(df)} rows -> {raw_path}")
    return df