"""
TimePicker для выбора произвольного времени напоминаний
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta


# ============ КЛАВИАТУРЫ ============

def get_time_picker_hours(selected_hour: int = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора часов (00-23)"""
    keyboard = []
    
    # Строки по 6 часов
    hours = list(range(24))
    for i in range(0, 24, 6):
        row = []
        for hour in hours[i:i+6]:
            label = f"{hour:02d}"
            if hour == selected_hour:
                label = f"✓{label}"
            row.append(InlineKeyboardButton(
                label, 
                callback_data=f"tp_hour:{hour}"
            ))
        keyboard.append(row)
    
    # Кнопка отмены
    keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="tp_cancel")])
    
    return InlineKeyboardMarkup(keyboard)


def get_time_picker_minutes(hour: int, selected_minute: int = None) -> InlineKeyboardMarkup:
    """Клавиатура выбора минут (00, 05, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55)"""
    keyboard = []
    
    # Шаг 5 минут для точности
    minutes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    
    for i in range(0, 12, 4):
        row = []
        for minute in minutes[i:i+4]:
            label = f"{minute:02d}"
            if minute == selected_minute:
                label = f"✓{label}"
            row.append(InlineKeyboardButton(
                label,
                callback_data=f"tp_min:{hour}:{minute}"
            ))
        keyboard.append(row)
    
    # Кнопка назад к часам + отмена
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад к часам", callback_data="tp_back_hours"),
        InlineKeyboardButton("❌ Отмена", callback_data="tp_cancel")
    ])
    
    return InlineKeyboardMarkup(keyboard)


def get_time_confirm_keyboard(hour: int, minute: int, date_str: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения выбранного времени"""
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data=f"tp_confirm:{hour}:{minute}")],
        [InlineKeyboardButton("🔄 Выбрать другое время", callback_data="tp_back_hours")],
        [InlineKeyboardButton("❌ Отмена", callback_data="tp_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ============ ОБРАБОТКА ВРЕМЕНИ ============

def calculate_reminder_time(hour: int, minute: int) -> tuple[datetime, str]:
    """
    Вычисляет время напоминания
    Возвращает: (datetime объект, строка описания даты)
    """
    now = datetime.now()
    selected_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    if selected_time <= now:
        # Время уже прошло — ставим на завтра
        selected_time += timedelta(days=1)
        date_str = "завтра"
    else:
        date_str = "сегодня"
    
    return selected_time, date_str


def format_time(hour: int, minute: int) -> str:
    """Форматирует время для отображения"""
    return f"{hour:02d}:{minute:02d}"


# ============ ТЕКСТЫ ============

def get_hour_selection_text() -> str:
    """Текст для выбора часа"""
    return "⏰ *Выберите час*\n\n(Московское время UTC+3)"


def get_minute_selection_text(hour: int) -> str:
    """Текст для выбора минут"""
    return f"⏰ Выбрано: *{hour:02d}:??*\n\nТеперь выберите минуты:"


def get_confirm_text(hour: int, minute: int, date_str: str) -> str:
    """Текст для подтверждения"""
    return (
        f"⏰ *{format_time(hour, minute)}*\n"
        f"📅 {date_str}\n\n"
        f"Подтвердить напоминание?"
    )
