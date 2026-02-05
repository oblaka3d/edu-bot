"""Database module for EduBot — SQLite and PostgreSQL support."""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try to import psycopg2
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

# Database configuration
DB_PATH = Path(__file__).parent.parent / "data" / "users.db"
DATABASE_URL = os.environ.get("DATABASE_URL")


def is_postgres() -> bool:
    """Check if PostgreSQL should be used."""
    return POSTGRES_AVAILABLE and DATABASE_URL is not None


def get_connection():
    """Get database connection (SQLite or PostgreSQL)."""
    if is_postgres():
        return psycopg2.connect(DATABASE_URL)
    else:
        DB_PATH.parent.mkdir(exist_ok=True)
        return sqlite3.connect(DB_PATH)


def get_cursor(conn):
    """Get cursor with appropriate factory."""
    if is_postgres():
        return conn.cursor(cursor_factory=RealDictCursor)
    else:
        conn.row_factory = sqlite3.Row
        return conn.cursor()


def dict_from_row(row) -> Optional[Dict[str, Any]]:
    """Convert row to dict regardless of database type."""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)


def init_db():
    """Initialize database with tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        # PostgreSQL syntax
        serial_type = "SERIAL"
        text_type = "TEXT"
        int_pk = "INTEGER PRIMARY KEY"
        auto_inc = "GENERATED ALWAYS AS IDENTITY"
        json_type = "JSONB"
        now_default = "DEFAULT NOW()"
    else:
        # SQLite syntax
        serial_type = "INTEGER"
        text_type = "TEXT"
        int_pk = "INTEGER PRIMARY KEY"
        auto_inc = "AUTOINCREMENT"
        json_type = "TEXT"
        now_default = ""
    
    # Users table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            user_id {int_pk},
            username {text_type},
            first_name {text_type},
            last_name {text_type},
            selected_track {text_type},
            current_stage INTEGER DEFAULT 0,
            current_topic INTEGER DEFAULT 0,
            joined_at {text_type},
            last_active {text_type}
        )
    """)
    
    # Progress table — completed topics
    if is_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                track TEXT,
                stage INTEGER,
                topic INTEGER,
                completed_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id, track, stage, topic)
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                track TEXT,
                stage INTEGER,
                topic INTEGER,
                completed_at TEXT,
                UNIQUE(user_id, track, stage, topic)
            )
        """)
    
    # Reminders table
    if is_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                track TEXT,
                schedule_type TEXT,
                days JSONB,
                time TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                track TEXT,
                schedule_type TEXT,
                days TEXT,
                time TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT
            )
        """)
    
    conn.commit()
    conn.close()
    
    if is_postgres():
        print("🐘 Using PostgreSQL database")
    else:
        print(f"🗄️  Using SQLite database at {DB_PATH}")


# ============ Users ============

def add_user(user_id: int, username: str, first_name: str, last_name: str):
    """Add new user."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    if is_postgres():
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, joined_at, last_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, username, first_name, last_name, now, now))
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name, joined_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, first_name, last_name, now, now))
    
    conn.commit()
    conn.close()


def update_last_active(user_id: int):
    """Update last active timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    if is_postgres():
        cursor.execute("""
            UPDATE users SET last_active = %s WHERE user_id = %s
        """, (now, user_id))
    else:
        cursor.execute("""
            UPDATE users SET last_active = ? WHERE user_id = ?
        """, (now, user_id))
    
    conn.commit()
    conn.close()


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user data."""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    if is_postgres():
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    else:
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict_from_row(row)


def set_user_track(user_id: int, track: str):
    """Set user's selected track."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        cursor.execute("""
            UPDATE users SET selected_track = %s WHERE user_id = %s
        """, (track, user_id))
    else:
        cursor.execute("""
            UPDATE users SET selected_track = ? WHERE user_id = ?
        """, (track, user_id))
    
    conn.commit()
    conn.close()


def update_user_progress(user_id: int, stage: int, topic: int):
    """Update user's current progress."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        cursor.execute("""
            UPDATE users SET current_stage = %s, current_topic = %s WHERE user_id = %s
        """, (stage, topic, user_id))
    else:
        cursor.execute("""
            UPDATE users SET current_stage = ?, current_topic = ? WHERE user_id = ?
        """, (stage, topic, user_id))
    
    conn.commit()
    conn.close()


# ============ Progress ============

def complete_topic(user_id: int, track: str, stage: int, topic: int):
    """Mark topic as completed."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    if is_postgres():
        cursor.execute("""
            INSERT INTO progress (user_id, track, stage, topic, completed_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, track, stage, topic) DO NOTHING
        """, (user_id, track, stage, topic, now))
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO progress (user_id, track, stage, topic, completed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, track, stage, topic, now))
    
    conn.commit()
    conn.close()


def get_completed_topics(user_id: int, track: str) -> List[Dict[str, Any]]:
    """Get list of completed topics for user and track."""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    if is_postgres():
        cursor.execute("""
            SELECT stage, topic, completed_at FROM progress 
            WHERE user_id = %s AND track = %s
            ORDER BY stage, topic
        """, (user_id, track))
    else:
        cursor.execute("""
            SELECT stage, topic, completed_at FROM progress 
            WHERE user_id = ? AND track = ?
            ORDER BY stage, topic
        """, (user_id, track))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict_from_row(row) for row in rows]


def get_completion_stats(user_id: int, track: str, total_topics: int) -> Dict[str, Any]:
    """Get completion statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        cursor.execute("""
            SELECT COUNT(*) FROM progress WHERE user_id = %s AND track = %s
        """, (user_id, track))
    else:
        cursor.execute("""
            SELECT COUNT(*) FROM progress WHERE user_id = ? AND track = ?
        """, (user_id, track))
    
    completed = cursor.fetchone()[0]
    conn.close()
    
    return {
        "completed": completed,
        "total": total_topics,
        "percentage": round((completed / total_topics * 100), 1) if total_topics > 0 else 0
    }


# ============ Reminders ============

def add_reminder(user_id: int, track: str, schedule_type: str, days: list, time: str):
    """Add reminder for user."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    # Deactivate existing reminders for this track
    if is_postgres():
        cursor.execute("""
            UPDATE reminders SET is_active = FALSE 
            WHERE user_id = %s AND track = %s
        """, (user_id, track))
        
        # Add new reminder
        cursor.execute("""
            INSERT INTO reminders (user_id, track, schedule_type, days, time, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, TRUE, %s)
        """, (user_id, track, schedule_type, json.dumps(days), time, now))
    else:
        cursor.execute("""
            UPDATE reminders SET is_active = 0 
            WHERE user_id = ? AND track = ?
        """, (user_id, track))
        
        cursor.execute("""
            INSERT INTO reminders (user_id, track, schedule_type, days, time, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, 1, ?)
        """, (user_id, track, schedule_type, json.dumps(days), time, now))
    
    conn.commit()
    conn.close()


def get_active_reminders(user_id: int) -> List[Dict[str, Any]]:
    """Get all active reminders for user."""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    if is_postgres():
        cursor.execute("""
            SELECT * FROM reminders WHERE user_id = %s AND is_active = TRUE
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT * FROM reminders WHERE user_id = ? AND is_active = 1
        """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    reminders = []
    for row in rows:
        reminder = dict_from_row(row)
        if reminder:
            days = reminder.get("days", "[]")
            if isinstance(days, str):
                reminder["days"] = json.loads(days) if days else []
            else:
                reminder["days"] = days
            reminders.append(reminder)
    
    return reminders


def get_reminders_for_time(day: str, time: str) -> List[Dict[str, Any]]:
    """Get all reminders that should fire at given day and time."""
    conn = get_connection()
    cursor = get_cursor(conn)
    
    if is_postgres():
        cursor.execute(
            "SELECT * FROM reminders WHERE is_active = TRUE AND time = %s",
            (time,)
        )
    else:
        cursor.execute(
            "SELECT * FROM reminders WHERE is_active = 1 AND time = ?",
            (time,)
        )
    
    rows = cursor.fetchall()
    conn.close()
    
    matching = []
    for row in rows:
        reminder = dict_from_row(row)
        if not reminder:
            continue
        
        days = reminder.get("days", "[]")
        if isinstance(days, str):
            reminder["days"] = json.loads(days) if days else []
        else:
            reminder["days"] = days
        
        schedule_type = reminder.get("schedule_type", "")
        days_list = reminder.get("days", [])
        
        should_fire = False
        if schedule_type == "weekdays" and day in ["mon", "tue", "wed", "thu", "fri"]:
            should_fire = True
        elif schedule_type == "weekends" and day in ["sat", "sun"]:
            should_fire = True
        elif schedule_type == "custom" and day in days_list:
            should_fire = True
        
        if should_fire:
            matching.append(reminder)
    
    return matching


def delete_reminder(reminder_id: int):
    """Delete reminder by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        cursor.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
    else:
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    
    conn.commit()
    conn.close()


def toggle_reminder(reminder_id: int, is_active: bool):
    """Toggle reminder active state."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_postgres():
        cursor.execute("""
            UPDATE reminders SET is_active = %s WHERE id = %s
        """, (is_active, reminder_id))
    else:
        cursor.execute("""
            UPDATE reminders SET is_active = ? WHERE id = ?
        """, (1 if is_active else 0, reminder_id))
    
    conn.commit()
    conn.close()
