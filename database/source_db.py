# database/source_db.py
import sqlite3
import os

DB_PATH = "users.db"

def init_source_table():
    try:
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
    except Exception:
        pass

def register_source(source_id, source_name, department, authority_tier):
    init_source_table()
    default_scores = {
        "Tier 1 (Authoritative Policy / Runbook)": 95.0,
        "Tier 2 (Internal Wiki / Confluence)": 80.0,
        "Tier 3 (Informal Chat / Draft)": 55.0
    }
    initial_score = default_scores.get(authority_tier, 75.0)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO source_reliability 
            (source_id, source_name, department, authority_tier, reliability_score)
            VALUES (?, ?, ?, ?, ?)
        """, (source_id, source_name, department, authority_tier, initial_score))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_source_score(source_id):
    init_source_table()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT reliability_score, authority_tier FROM source_reliability WHERE source_id = ?", (source_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0], row[1]
    except Exception:
        pass
    return 80.0, "Tier 2 (Internal Wiki / Confluence)"

def update_source_feedback(source_id, is_positive=True):
    init_source_table()
    delta = 2.5 if is_positive else -6.0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Ensure row exists first
        cursor.execute("SELECT source_id FROM source_reliability WHERE source_id = ?", (source_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO source_reliability (source_id, source_name, department, authority_tier, reliability_score) VALUES (?, ?, ?, ?, ?)", (source_id, source_id, "General", "Tier 1", 95.0))
            
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
    except Exception:
        pass
