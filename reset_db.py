"""
reset_db.py
-----------
Wipes all analysis data so you can re-upload your CSV and get
clean, deduplicated results with the fixed pipeline.

Run with:
    python reset_db.py
"""
import sqlite3

DB_PATH = "feedback_analysis.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

tables = ["reasoning_traces", "recommendations", "bias_checks", "theme_assignments", "sentiment_analysis", "feedback"]

print("Clearing all analysis tables...")
for table in tables:
    try:
        cur.execute(f"DELETE FROM {table}")
        print(f"  Cleared: {table}")
    except sqlite3.OperationalError:
        print(f"  Skipped (missing): {table}")

conn.commit()

print("\nVerifying counts after reset:")
for table in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {cur.fetchone()[0]} rows")
    except sqlite3.OperationalError:
        print(f"  {table}: (table not present)")

conn.close()
print("\nDone. Re-upload your CSV - no more duplicates!")
