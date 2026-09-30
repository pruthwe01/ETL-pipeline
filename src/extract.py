import math
import random
import time
from pathlib import Path

import pandas as pd
from ckanapi import RemoteCKAN

PORTAL_URL = "https://data.gov.au/data/"
RESOURCE_ID = "591cb009-1167-4008-b7e8-f5fc9dbbb511"
RAW_DIR = Path("data/raw")
BLOCK_SIZE = 1000


def extract_placements(sample_size=50000, seed=42):
    """Download a block-sampled subset of the table and save the raw rows."""
    rc = RemoteCKAN(PORTAL_URL)

    # Ask for one row just to learn how big the table is
    total = rc.action.datastore_search(resource_id=RESOURCE_ID, limit=1)["total"]

    # Choose which blocks of the table to download
    n_blocks = math.ceil(sample_size / BLOCK_SIZE)
    all_starts = list(range(0, total, BLOCK_SIZE))
    rng = random.Random(seed)
    starts = sorted(rng.sample(all_starts, min(n_blocks, len(all_starts))))

    rows = []
    for i, start in enumerate(starts, 1):
        result = rc.action.datastore_search(
            resource_id=RESOURCE_ID,
            limit=BLOCK_SIZE,
            offset=start,
            sort="_id asc",
        )
        rows.extend(result["records"])
        print(f"Block {i} of {len(starts)} (offset {start}): {len(rows)} rows so far")
        time.sleep(0.5)  # be polite to the server

    df = pd.DataFrame(rows)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "job_placements_raw.csv"
    df.to_csv(raw_path, index=False)
    print(f"Saved {len(df)} rows (sampled from {total}) -> {raw_path}")
    return df