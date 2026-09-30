import sqlite3
from pathlib import Path

DB_PATH = Path("data/jobs.db")


def load_placements(df):
    """Write the clean table to SQLite, replacing any previous version."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        df.to_sql("job_placements", conn, if_exists="replace", index=False)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_state ON job_placements(state)"
        )
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM job_placements").fetchone()[0]
    finally:
        conn.close()
    print(f"Loaded {count} rows into {DB_PATH}")