import sqlite3

DB_PATH = "chat_history.db"

def init_memory_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_memory (
            username TEXT PRIMARY KEY,
            memory_data TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_memory_db()

def save_profile_memory(username, memory_text):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_memory (username, memory_data)
            VALUES (?, ?)
            ON CONFLICT(username) DO UPDATE SET memory_data=excluded.memory_data
        ''', (username, str(memory_text)))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_profile_memory(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT memory_data FROM user_memory WHERE username = ?', (username,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else ""
    except Exception:
        return ""
