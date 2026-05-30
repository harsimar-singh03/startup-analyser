import sqlite3
import json
import uuid
from datetime import datetime

DB_FILE = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            thread_id TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(thread_id, role, message):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chats VALUES (?, ?, ?, ?)",
        (thread_id, role, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def load_history(thread_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT role, message FROM chats WHERE thread_id=? ORDER BY timestamp",
        (thread_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "message": m} for r, m in rows]

def get_all_threads():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT thread_id, startup_idea
        FROM research
        ORDER BY rowid DESC
    """)
    rows = c.fetchall()
    conn.close()

    threads = []
    for thread_id, startup_idea in rows:
        # Take first 5 words of the startup idea as title
        words = startup_idea.strip().split()
        short_title = " ".join(words[:5])
        if len(words) > 5:
            short_title += "..."
        threads.append({
            "thread_id": thread_id,
            "title": short_title
        })

    return threads

def new_thread_id():
    return str(uuid.uuid4())


def save_research(thread_id, startup_idea, tool_outputs):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS research (
            thread_id TEXT PRIMARY KEY,
            startup_idea TEXT,
            tool_outputs TEXT
        )
    """)
    c.execute(
        "INSERT OR REPLACE INTO research VALUES (?, ?, ?)",
        (thread_id, startup_idea, json.dumps(tool_outputs))
    )
    conn.commit()
    conn.close()

def load_research(thread_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS research (
            thread_id TEXT PRIMARY KEY,
            startup_idea TEXT,
            tool_outputs TEXT
        )
    """)
    c.execute(
        "SELECT startup_idea, tool_outputs FROM research WHERE thread_id=?",
        (thread_id,)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "startup_idea": row[0],
            "tool_outputs": json.loads(row[1])
        }
    return None