import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.expanduser("~/.fisch_macro/j_macro.db")

class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        schema_path = os.path.join(os.path.dirname(__file__), "../data/schema.sql")
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                self.cursor.executescript(f.read())
            self.conn.commit()

    def set_setting(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        self.conn.commit()

    def get_setting(self, key, default=None):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else default

    def log_event(self, level, message):
        self.cursor.execute("INSERT INTO event_log (level, message) VALUES (?, ?)", (level, message))
        self.conn.commit()

    def add_history(self, event_type, details):
        self.cursor.execute("INSERT INTO session_history (event_type, details) VALUES (?, ?)", (event_type, details))
        self.conn.commit()

    def create_checkpoint(self, state_dict):
        state_json = json.dumps(state_dict)
        self.cursor.execute("INSERT INTO checkpoints (state_json) VALUES (?)", (state_json,))
        self.conn.commit()

    def get_last_checkpoint(self):
        self.cursor.execute("SELECT state_json FROM checkpoints ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchone()
        return json.loads(row[0]) if row else None

    def close(self):
        self.conn.close()

# Singleton instance
db = Database()
