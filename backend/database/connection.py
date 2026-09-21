import os
import sqlite3

# Define database path (uses /tmp on Vercel to allow writes in serverless environment)
if os.environ.get("VERCEL") == "1":
    DB_PATH = "/tmp/leave_automation.db"
else:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DB_PATH = os.path.join(PROJECT_ROOT, "leave_automation.db")


def get_connection():
    """Returns a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # Enable foreign keys for referential integrity
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
