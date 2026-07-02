import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/bro.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        self.conn.commit()

    # ---------- История ----------

    def add_message(self, role: str, message: str):
        self.cursor.execute(
            "INSERT INTO history(role, message) VALUES(?, ?)",
            (role, message)
        )
        self.conn.commit()

    def get_history(self, limit=20):
        self.cursor.execute(
            """
            SELECT role, message
            FROM history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return list(reversed(self.cursor.fetchall()))

    # ---------- Факты ----------

    def set_fact(self, key: str, value: str):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO facts(key, value)
            VALUES(?, ?)
            """,
            (key, value)
        )

        self.conn.commit()

    def get_fact(self, key: str):
        self.cursor.execute(
            "SELECT value FROM facts WHERE key=?",
            (key,)
        )

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

    def get_all_facts(self):
        self.cursor.execute(
            "SELECT key, value FROM facts"
        )

        return dict(self.cursor.fetchall())