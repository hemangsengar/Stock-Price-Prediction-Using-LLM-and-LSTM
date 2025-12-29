import sqlite3
import json
import time
from datetime import datetime, timedelta

class AnalysisCache:
    def __init__(self, db_path="analysis_cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cache (
                        ticker TEXT PRIMARY KEY,
                        data TEXT,
                        timestamp DATETIME
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"❌ Cache DB Init Error: {e}")

    def get(self, ticker, expiry_hours=6):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT data, timestamp FROM cache WHERE ticker = ?", (ticker,))
                row = cursor.fetchone()
                if row:
                    data_str, ts_str = row
                    timestamp = datetime.fromisoformat(ts_str)
                    if datetime.now() - timestamp < timedelta(hours=expiry_hours):
                        return json.loads(data_str)
        except sqlite3.OperationalError:
            self._init_db() # Self-heal if table missing
        except Exception as e:
            print(f"❌ Cache Get Error: {e}")
        return None

    def set(self, ticker, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (ticker, data, timestamp) VALUES (?, ?, ?)",
                (ticker, json.dumps(data), datetime.now().isoformat())
            )

cache = AnalysisCache()
