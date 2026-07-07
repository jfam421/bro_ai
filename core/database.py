import sqlite3
from pathlib import Path


class Database:

    HISTORY_LIMIT = 10

    def __init__(self):
        Path("data").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("data/bro.db")
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL UNIQUE,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

        self._memory_cache = None

    # ==========================================================
    # История
    # ==========================================================

    def add_message(self, role: str, message: str):
        self.cursor.execute(
            "INSERT INTO history(role, message) VALUES(?, ?)",
            (role, message)
        )

        # Храним только последние HISTORY_LIMIT сообщений
        self.cursor.execute(
            """
            DELETE FROM history
            WHERE id NOT IN (
                SELECT id
                FROM history
                ORDER BY id DESC
                LIMIT ?
            )
            """,
            (self.HISTORY_LIMIT,)
        )

        self.conn.commit()

    def get_history(self, limit=None):

        if limit is None:
            limit = self.HISTORY_LIMIT

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

    # ==========================================================
    # Старые факты
    # ==========================================================

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

        return row[0] if row else None

    def get_all_facts(self):
        self.cursor.execute(
            "SELECT key, value FROM facts"
        )

        return dict(self.cursor.fetchall())

    # ==========================================================
    # Память
    # ==========================================================

    def add_memory(self, fact: str):

        fact = fact.strip()

        if not fact:
            return

        if self._memory_cache is None:
            self.get_memory()

        if fact in self._memory_cache:
            return

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO memory(fact)
            VALUES(?)
            """,
            (fact,)
        )

        self.conn.commit()

        self._memory_cache.append(fact)

    def get_memory(self):

        if self._memory_cache is not None:
            return self._memory_cache

        self.cursor.execute(
            """
            SELECT fact
            FROM memory
            ORDER BY id
            """
        )

        self._memory_cache = [
            row[0]
            for row in self.cursor.fetchall()
        ]

        return self._memory_cache

    def clear_memory(self):
        self.cursor.execute(
            "DELETE FROM memory"
        )

        self.conn.commit()

        self._memory_cache = []