import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/pages.db")

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            url TEXT PRIMARY KEY,
            title TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_page(url, title, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO pages (url, title, content) VALUES (?, ?, ?)",
                   (url, title, content))
    conn.commit()
    conn.close()

def load_pages():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM pages", conn)
    conn.close()
    return df

