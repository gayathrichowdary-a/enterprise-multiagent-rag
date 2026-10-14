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

# Alias so both register_user and create_user work seamlessly
def register_user(username, email, password):
    return create_user(username, email, password)

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

# ---- NEW: read the saved email back from the database ----
def get_user_email(username):
    """Return the email saved for this username (or email), or '' if not found."""
    create_database()
    val = (username or "").strip().lower()
    if not val:
        return ""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username = ? OR email = ?", (val, val))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else ""

def get_user(username):
    """Return a dict with username and email for this user, or None if not found."""
    create_database()
    val = (username or "").strip().lower()
    if not val:
        return None
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, email FROM users WHERE username = ? OR email = ?", (val, val))
    row = c.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "email": row[1]}
    return None