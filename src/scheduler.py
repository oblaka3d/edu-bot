"""Scheduler module for sending reminders."""

import threading
import time
from datetime import datetime
from typing import Callable

from database import get_reminders_for_time, get_user, update_user_progress
from roadmaps import parse_roadmap, format_topic_for_display


# Callback function for sending messages
default_send_callback: Callable[[int, str], None] = None


def set_send_callback(callback: Callable[[int, str], None]):
    """Set callback function for sending messages."""
    global default_send_callback
    default_send_callback = callback


def get_day_name() -> str:
    """Get current day abbreviation."""
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    return days[datetime.now().weekday()]


def check_and_send_reminders():
    """Check for reminders that should fire now and send them."""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_day = get_day_name()
    
    reminders = get_reminders_for_time(current_day, current_time)
    
    if not reminders or not default_send_callback:
        return
    
    for reminder in reminders:
        user_id = reminder["user_id"]
        track = reminder["track"]
        
        # Get user data
        user = get_user(user_id)
        if not user:
            continue
        
        # Check if user has this track selected
        if user.get("selected_track") != track:
            continue
        
        # Get current topic
        stage = user.get("current_stage", 0)
        topic_idx = user.get("current_topic", 0)
        
        # Parse roadmap
        roadmap = parse_roadmap(track)
        if not roadmap:
            continue
        
        # Find current topic
        current_topic = None
        total_in_stage = 0
        for s in roadmap.stages:
            if s.number == stage:
                total_in_stage = len(s.topics)
                for t in s.topics:
                    if t.topic_num == topic_idx:
                        current_topic = t
                        break
        
        if not current_topic:
            continue
        
        # Format and send reminder
        message = (
            f"⏰ *Время учиться!*\n\n"
            f"{format_topic_for_display(current_topic, total_in_stage)}\n"
            f"💡 Открой бота, чтобы продолжить обучение!"
        )
        
        try:
            default_send_callback(user_id, message)
        except Exception as e:
            print(f"Failed to send reminder to {user_id}: {e}")


def scheduler_loop():
    """Main scheduler loop — runs in background thread."""
    while True:
        try:
            check_and_send_reminders()
        except Exception as e:
            print(f"Scheduler error: {e}")
        
        # Check every minute
        time.sleep(60)


def start_scheduler(send_callback: Callable[[int, str], None]):
    """Start reminder scheduler in background thread."""
    set_send_callback(send_callback)
    
    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()
    print("📅 Reminder scheduler started")


def format_days_display(schedule_type: str, days: list) -> str:
    """Format days for display."""
    day_names = {
        "mon": "Пн", "tue": "Вт", "wed": "Ср", 
        "thu": "Чт", "fri": "Пт", "sat": "Сб", "sun": "Вс"
    }
    
    if schedule_type == "weekdays":
        return "Будние дни (Пн–Пт)"
    elif schedule_type == "weekends":
        return "Выходные (Сб–Вс)"
    elif schedule_type == "custom":
        return ", ".join(day_names.get(d, d) for d in days)
    return schedule_type
