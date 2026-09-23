import sqlite3
import hashlib

DB_FILE = "users.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def create_database():
    conn = get_connection()
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
    conn.close()

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(username, email, password):
    create_database()
    u = username.strip().lower()
    e = email.strip().lower()
    if not u or not e or not password:
        return False, "All fields are required."
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? OR email = ?", (u, e))
    if c.fetchone():
        conn.close()
        return False, "An account with this username or email already exists."
    
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (u, e, hash_pw(password)))
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except Exception as err:
        conn.close()
        return False, f"Database error: {str(err)}"

def verify_user(username_or_email, password):
    create_database()
    val = username_or_email.strip().lower()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE username = ? OR email = ?", (val, val))
    row = c.fetchone()
    conn.close()
    if row and row[1] == hash_pw(password):
        return True, row[0]
    return False, None
