import sqlite3
import os

DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_chat_message(username, role, message):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO messages (username, role, message) VALUES (?, ?, ?)', (username, role, message))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_chat_history(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT role, message FROM messages WHERE username = ? ORDER BY id ASC', (username,))
        rows = c.fetchall()
        conn.close()
        return [{"role": r[0], "message": r[1]} for r in rows]
    except Exception:
        return []

def clear_chat_history(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM messages WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    except Exception:
        pass
