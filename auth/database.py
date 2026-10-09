import sqlite3
import hashlib
import os

DB_FILE = "users.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_database():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
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

def create_user(username: str, email: str, password: str):
    create_database()
    u = username.strip().lower()
    e = email.strip().lower()
    p = password.strip()
    
    if not u or not e or not p:
        return False, "All fields are required."
    
    if len(p) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? OR email = ?", (u, e))
    if c.fetchone():
        conn.close()
        return False, "An account with this username or email already exists."
    
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (u, e, hash_pw(p)))
        conn.commit()
        conn.close()
        return True, "Account created successfully! Please log in."
    except Exception as err:
        conn.close()
        return False, f"Database error: {str(err)}"

def verify_user(username_or_email: str, password: str):
    create_database()
    val = username_or_email.strip().lower()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, email, password_hash FROM users WHERE username = ? OR email = ?", (val, val))
    row = c.fetchone()
    conn.close()
    
    if row and row[2] == hash_pw(password):
        return True, row[0], row[1]
    return False, None, None