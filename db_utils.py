"""
Database utilities for WindyAI
Using SQLite for better performance and scalability
"""
import sqlite3
import os
from datetime import datetime
import json

DB_FILE = "smarttravel.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            destination TEXT NOT NULL,
            budget REAL NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            timeline_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_schedule_user ON schedules(user_id)')
    
    conn.commit()
    conn.close()

def add_user(email, password):
    """Add a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        return False, None

def get_user(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def verify_user(email, password):
    """Verify user credentials"""
    user = get_user(email)
    if user and user['password'] == password:
        return True, user['id']
    return False, None

def add_schedule(user_id, destination, budget, start_time, end_time, timeline):
    """Add a new schedule for user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert timeline list to JSON string
    timeline_json = json.dumps(timeline, ensure_ascii=False)
    
    cursor.execute('''
        INSERT INTO schedules (user_id, destination, budget, start_time, end_time, timeline_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, destination, budget, start_time, end_time, timeline_json))
    
    conn.commit()
    schedule_id = cursor.lastrowid
    conn.close()
    return schedule_id

def get_user_schedules(user_id):
    """Get all schedules for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM schedules 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,))
    
    schedules = cursor.fetchall()
    conn.close()
    
    # Convert to list of dicts and parse JSON timeline
    result = []
    for schedule in schedules:
        schedule_dict = dict(schedule)
        schedule_dict['timeline'] = json.loads(schedule_dict['timeline_json'])
        del schedule_dict['timeline_json']  # Remove raw JSON field
        result.append(schedule_dict)
    
    return result

def delete_schedule(schedule_id, user_id):
    """Delete a schedule (with user ownership check)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM schedules 
        WHERE id = ? AND user_id = ?
    ''', (schedule_id, user_id))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def migrate_from_json(json_file="database.json"):
    """Migrate data from JSON to SQLite (one-time migration)"""
    if not os.path.exists(json_file):
        return False, "JSON file not found"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        users_data = data.get('users', {})
        user_data = data.get('user_data', {})
        
        # Migrate users
        email_to_id = {}
        for email, password in users_data.items():
            success, user_id = add_user(email, password)
            if success:
                email_to_id[email] = user_id
        
        # Migrate schedules
        for email, udata in user_data.items():
            if email in email_to_id:
                user_id = email_to_id[email]
                schedules = udata.get('schedules', [])
                
                for schedule in schedules:
                    add_schedule(
                        user_id=user_id,
                        destination=schedule.get('destination', 'Unknown'),
                        budget=schedule.get('budget', 0),
                        start_time=schedule.get('start_time', ''),
                        end_time=schedule.get('end_time', ''),
                        timeline=schedule.get('timeline', [])
                    )
        
        return True, f"Migrated {len(email_to_id)} users successfully"
    
    except Exception as e:
        return False, f"Migration error: {str(e)}"
