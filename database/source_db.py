# database/source_db.py
import sqlite3
import os

DB_PATH = "users.db"

def init_source_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS source_reliability (
            source_id TEXT PRIMARY KEY,
            source_name TEXT NOT NULL,
            department TEXT NOT NULL,
            authority_tier TEXT NOT NULL,
            reliability_score REAL DEFAULT 80.0,
            total_queries INTEGER DEFAULT 0,
            positive_feedback INTEGER DEFAULT 0,
            negative_feedback INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_source(source_id, source_name, department, authority_tier):
    # Tier 1 defaults to 95, Tier 2 to 80, Tier 3 to 55
    default_scores = {
        "Tier 1 (Authoritative Policy / Runbook)": 95.0,
        "Tier 2 (Internal Wiki / Confluence)": 80.0,
        "Tier 3 (Informal Chat / Draft)": 55.0
    }
    initial_score = default_scores.get(authority_tier, 75.0)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO source_reliability 
        (source_id, source_name, department, authority_tier, reliability_score)
        VALUES (?, ?, ?, ?, ?)
    """, (source_id, source_name, department, authority_tier, initial_score))
    conn.commit()
    conn.close()

def get_source_score(source_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT reliability_score, authority_tier FROM source_reliability WHERE source_id = ?", (source_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return 70.0, "Tier 2 (Internal Wiki / Confluence)"

def update_source_feedback(source_id, is_positive=True):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    delta = 2.5 if is_positive else -6.0
    cursor.execute("""
        UPDATE source_reliability 
        SET total_queries = total_queries + 1,
            positive_feedback = positive_feedback + CASE WHEN ? THEN 1 ELSE 0 END,
            negative_feedback = negative_feedback + CASE WHEN ? THEN 0 ELSE 1 END,
            reliability_score = MAX(15.0, MIN(100.0, reliability_score + ?)),
            last_updated = CURRENT_TIMESTAMP
        WHERE source_id = ?
    """, (is_positive, is_positive, delta, source_id))
    conn.commit()
    conn.close()

def get_all_sources():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM source_reliability ORDER BY reliability_score DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows