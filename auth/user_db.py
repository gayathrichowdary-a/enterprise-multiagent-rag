import sqlite3
import hashlib

DB_FILE = 'users.db'

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

get_db()

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(username, email, password):
    username = username.strip().lower()
    email = email.strip().lower()
    if not username or not email or not password:
        return False, "All fields are required."
        
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if c.fetchone():
        conn.close()
        return False, "Username or email already registered."
        
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (username, email, hash_pw(password)))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except Exception as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def verify_user(username_or_email, password):
    val = username_or_email.strip().lower()
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE username = ? OR email = ?", (val, val))
    row = c.fetchone()
    conn.close()
    if row and row[1] == hash_pw(password):
        return True, row[0]
    return False, None
