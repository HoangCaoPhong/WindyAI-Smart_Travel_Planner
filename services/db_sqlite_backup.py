"""
Database utilities for WindyAI
Using SQLite for local storage (easier setup than Supabase)
"""
import sqlite3
import json
import bcrypt
import os
from datetime import datetime

DB_FILE = "windyai.db"

def get_connection():
    """Get SQLite connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize SQLite database tables"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create schedules table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            destination TEXT,
            budget REAL,
            start_time TEXT,
            end_time TEXT,
            timeline_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        conn.commit()
        conn.close()
        print("✅ SQLite Database initialized")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

def add_user(email, password):
    """Add a new user with hashed password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already registered"
            
    except Exception as e:
        return False, str(e)

def get_user(email):
    """Get user by email"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def verify_user(email, password):
    """Verify user credentials"""
    user = get_user(email)
    if user:
        stored_password = user['password']
        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, user['id']
        except ValueError:
            # Fallback for plain text
            if stored_password == password:
                return True, user['id']
    return False, None

def add_schedule(user_id, destination, budget, start_time, end_time, timeline):
    """Add a new schedule"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        timeline_str = json.dumps(timeline, ensure_ascii=False)
        
        cursor.execute("""
            INSERT INTO schedules (user_id, destination, budget, start_time, end_time, timeline_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, destination, budget, start_time, end_time, timeline_str))
        
        schedule_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return schedule_id
    except Exception as e:
        print(f"Error adding schedule: {e}")
        return None

def get_user_schedules(user_id):
    """Get all schedules for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM schedules 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        schedules = []
        for row in rows:
            item = dict(row)
            item['timeline'] = json.loads(item['timeline_json'])
            schedules.append(item)
            
        conn.close()
        return schedules
    except Exception as e:
        print(f"Error getting schedules: {e}")
        return []

def delete_schedule(schedule_id, user_id):
    """Delete a schedule"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM schedules WHERE id = ? AND user_id = ?", (schedule_id, user_id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return False

def migrate_from_json(json_file="database.json"):
    """Migrate data from JSON to SQLite"""
    if not os.path.exists(json_file):
        return False, "JSON file not found"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        users_data = data.get('users', {})
        user_data = data.get('user_data', {})
        
        init_database()
        
        email_to_id = {}
        for email, password in users_data.items():
            existing = get_user(email)
            if not existing:
                success, user_id = add_user(email, password)
                if success:
                    email_to_id[email] = user_id
            else:
                email_to_id[email] = existing['id']
        
        count = 0
        for email, udata in user_data.items():
            if email in email_to_id:
                user_id = email_to_id[email]
                schedules = udata.get('schedules', [])
                for schedule in schedules:
                    add_schedule(
                        user_id,
                        schedule.get('destination', 'Unknown'),
                        schedule.get('budget', 0),
                        schedule.get('start_time', ''),
                        schedule.get('end_time', ''),
                        schedule.get('timeline', [])
                    )
                    count += 1
                    
        return True, f"Migrated {count} schedules"
    except Exception as e:
        return False, str(e)

