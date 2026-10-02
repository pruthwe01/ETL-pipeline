import sqlite3

import pandas as pd

import sqlite3

import pandas as pd

from src.extract import extract_placements
from src.transform import transform_placements
from src.validate import validate_placements
from src.load import load_placements

if __name__ == "__main__":
    raw = extract_placements(sample_size=50000)
    clean = transform_placements(raw)

    errors, warnings = validate_placements(clean)
    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        raise SystemExit("Validation failed, nothing was loaded.")

    load_placements(clean)

    conn = sqlite3.connect("data/jobs.db")
    query = """
        SELECT state, COUNT(*) AS placements
        FROM job_placements
        GROUP BY state
        ORDER BY placements DESC
    """
    print(pd.read_sql(query, conn))
    conn.close()