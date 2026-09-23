# database/profile_memory.py
import sqlite3
import os

DB_PATH = os.path.join("database", "users.db") if os.path.exists("database") else "users.db"

def _extract_user_id(user_val):
    """Safely extracts a scalar user_id if passed a tuple or dictionary."""
    if isinstance(user_val, (tuple, list)):
        return str(user_val[0])
    elif isinstance(user_val, dict):
        return str(user_val.get("id", user_val.get("user_id", "default")))
    return str(user_val)

def init_profile_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_memory (
            user_id TEXT,
            key TEXT,
            value TEXT,
            PRIMARY KEY (user_id, key)
        )
    """)
    conn.commit()
    conn.close()

def save_profile_memory(user_id, key, value):
    uid = _extract_user_id(user_id)
    init_profile_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO profile_memory (user_id, key, value)
        VALUES (?, ?, ?)
    """, (uid, str(key), str(value)))
    conn.commit()
    conn.close()

def load_profile_memory(user_id):
    uid = _extract_user_id(user_id)
    init_profile_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM profile_memory WHERE user_id = ?", (uid,))
    rows = cursor.fetchall()
    conn.close()
    return {k: v for k, v in rows}