"""
Feedback Service using Supabase
"""
import pandas as pd
from services.db import supabase
from services import db_sqlite_backup as local_db

def init_feedback_db():
    """Initialize the feedback database table."""
    if supabase:
        return
    with local_db.get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT, category TEXT,
            content TEXT NOT NULL, status TEXT DEFAULT 'New',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def add_feedback(name, email, category, content):
    """Add a new feedback entry."""
    if not supabase:
        init_feedback_db()
        with local_db.get_connection() as conn:
            conn.execute(
                "INSERT INTO feedback (name, email, category, content, status) VALUES (?, ?, ?, ?, ?)",
                (name, email, category, content, "New"),
            )
        return True

    try:
        data = {
            "name": name,
            "email": email,
            "category": category,
            "content": content,
            "status": "New"
        }
        supabase.table("feedback").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error adding feedback: {e}")
        return False

def get_all_feedback():
    """Retrieve all feedback entries."""
    if not supabase:
        init_feedback_db()
        with local_db.get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM feedback ORDER BY id DESC", conn)
        if not df.empty:
            df["timestamp"] = df["created_at"]
        return df

    try:
        response = supabase.table("feedback").select("*").order("id", desc=True).execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            # Map created_at to timestamp for compatibility
            if 'created_at' in df.columns:
                df['timestamp'] = df['created_at']
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return pd.DataFrame()
