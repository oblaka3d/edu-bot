"""Database module for EduBot — SQLite operations."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

DB_PATH = Path(__file__).parent.parent / "data" / "users.db"


def init_db():
    """Initialize database with tables."""
    DB_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            selected_track TEXT,
            current_stage INTEGER DEFAULT 0,
            current_topic INTEGER DEFAULT 0,
            joined_at TEXT,
            last_active TEXT
        )
    """)
    
    # Progress table — completed topics
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            track TEXT,
            schedule_type TEXT,  -- 'weekdays', 'weekends', 'custom'
            days TEXT,  -- JSON list for custom ["mon", "wed", "fri"]
            time TEXT,  -- "HH:MM" format
            is_active INTEGER DEFAULT 1,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def get_connection():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


# ============ Users ============

def add_user(user_id: int, username: str, first_name: str, last_name: str):
    """Add new user."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
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
    
    cursor.execute("""
        UPDATE users SET last_active = ? WHERE user_id = ?
    """, (now, user_id))
    
    conn.commit()
    conn.close()


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user data."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def set_user_track(user_id: int, track: str):
    """Set user's selected track."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users SET selected_track = ? WHERE user_id = ?
    """, (track, user_id))
    
    conn.commit()
    conn.close()


def update_user_progress(user_id: int, stage: int, topic: int):
    """Update user's current progress."""
    conn = get_connection()
    cursor = conn.cursor()
    
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
    
    cursor.execute("""
        INSERT OR IGNORE INTO progress (user_id, track, stage, topic, completed_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, track, stage, topic, now))
    
    conn.commit()
    conn.close()


def get_completed_topics(user_id: int, track: str) -> List[Dict[str, Any]]:
    """Get list of completed topics for user and track."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT stage, topic, completed_at FROM progress 
        WHERE user_id = ? AND track = ?
        ORDER BY stage, topic
    """, (user_id, track))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_completion_stats(user_id: int, track: str, total_topics: int) -> Dict[str, Any]:
    """Get completion statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
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
    cursor.execute("""
        UPDATE reminders SET is_active = 0 
        WHERE user_id = ? AND track = ?
    """, (user_id, track))
    
    # Add new reminder
    cursor.execute("""
        INSERT INTO reminders (user_id, track, schedule_type, days, time, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, 1, ?)
    """, (user_id, track, schedule_type, json.dumps(days), time, now))
    
    conn.commit()
    conn.close()


def get_active_reminders(user_id: int) -> List[Dict[str, Any]]:
    """Get all active reminders for user."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM reminders WHERE user_id = ? AND is_active = 1
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    reminders = []
    for row in rows:
        reminder = dict(row)
        reminder["days"] = json.loads(reminder["days"]) if reminder["days"] else []
        reminders.append(reminder)
    
    return reminders


def get_reminders_for_time(day: str, time: str) -> List[Dict[str, Any]]:
    """Get all reminders that should fire at given day and time."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all active reminders
    cursor.execute("SELECT * FROM reminders WHERE is_active = 1 AND time = ?", (time,))
    rows = cursor.fetchall()
    conn.close()
    
    matching = []
    for row in rows:
        reminder = dict(row)
        reminder["days"] = json.loads(reminder["days"]) if reminder["days"] else []
        
        schedule_type = reminder["schedule_type"]
        days = reminder["days"]
        
        should_fire = False
        if schedule_type == "weekdays" and day in ["mon", "tue", "wed", "thu", "fri"]:
            should_fire = True
        elif schedule_type == "weekends" and day in ["sat", "sun"]:
            should_fire = True
        elif schedule_type == "custom" and day in days:
            should_fire = True
        
        if should_fire:
            matching.append(reminder)
    
    return matching


def delete_reminder(reminder_id: int):
    """Delete reminder by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    
    conn.commit()
    conn.close()


def toggle_reminder(reminder_id: int, is_active: bool):
    """Toggle reminder active state."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE reminders SET is_active = ? WHERE id = ?
    """, (1 if is_active else 0, reminder_id))
    
    conn.commit()
    conn.close()
