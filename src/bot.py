"""EduBot — Telegram bot for structured learning with reminders."""

import os
import sys
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler
)

from database import (
    init_db, add_user, get_user, update_last_active,
    set_user_track, update_user_progress, complete_topic,
    get_completed_topics, get_completion_stats,
    add_reminder, get_active_reminders, delete_reminder
)
from roadmaps import (
    parse_roadmap, get_all_tracks, format_topic_for_display,
    get_track_display_name
)
from scheduler import start_scheduler, format_days_display

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
SELECTING_TRACK, SELECTING_SCHEDULE_TYPE, SELECTING_DAYS, SELECTING_TIME = range(4)

# ============== Helper Functions ==============

def get_main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Get main menu keyboard based on user state."""
    user = get_user(user_id)
    
    if not user or not user.get("selected_track"):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Выбрать направление", callback_data="select_track")],
        ])
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Продолжить обучение", callback_data="continue_learning")],
        [InlineKeyboardButton("📊 Мой прогресс", callback_data="show_progress")],
        [InlineKeyboardButton("⏰ Настроить напоминания", callback_data="setup_reminders")],
        [InlineKeyboardButton("🔄 Сменить направление", callback_data="select_track")],
    ])


def get_topic_keyboard(track: str, stage: int, topic_num: int, is_last: bool = False) -> InlineKeyboardMarkup:
    """Get keyboard for topic view."""
    buttons = [
        [
            InlineKeyboardButton("✅ Пройдено — дальше", callback_data=f"complete|{track}|{stage}|{topic_num}"),
        ],
        [
            InlineKeyboardButton("📊 Прогресс", callback_data="show_progress"),
            InlineKeyboardButton("⏸️ Главное меню", callback_data="main_menu"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def get_schedule_type_keyboard() -> InlineKeyboardMarkup:
    """Get schedule type selection keyboard."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Будние дни (Пн–Пт)", callback_data="stype|weekdays")],
        [InlineKeyboardButton("🌴 Выходные (Сб–Вс)", callback_data="stype|weekends")],
        [InlineKeyboardButton("⚙️ Выбрать дни", callback_data="stype|custom")],
        [InlineKeyboardButton("❌ Отмена", callback_data="main_menu")],
    ])


def get_days_keyboard(selected: list = None) -> InlineKeyboardMarkup:
    """Get days selection keyboard."""
    if selected is None:
        selected = []
    
    days = [
        ("mon", "Пн"), ("tue", "Вт"), ("wed", "Ср"),
        ("thu", "Чт"), ("fri", "Пт"), ("sat", "Сб"), ("sun", "Вс")
    ]
    
    rows = []
    row = []
    for day_code, day_name in days:
        prefix = "✅ " if day_code in selected else ""
        row.append(InlineKeyboardButton(
            f"{prefix}{day_name}", 
            callback_data=f"day|{day_code}"
        ))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    
    rows.append([
        InlineKeyboardButton("✅ Сохранить", callback_data="days_done"),
        InlineKeyboardButton("❌ Отмена", callback_data="main_menu"),
    ])
    
    return InlineKeyboardMarkup(rows)


def get_time_keyboard() -> InlineKeyboardMarkup:
    """Get time selection keyboard."""
    times = ["09:00", "10:00", "12:00", "15:00", "18:00", "19:00", "20:00", "21:00"]
    
    rows = []
    row = []
    for t in times:
        row.append(InlineKeyboardButton(t, callback_data=f"time|{t}"))
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    
    rows.append([InlineKeyboardButton("❌ Отмена", callback_data="main_menu")])
    return InlineKeyboardMarkup(rows)


# ============== Command Handlers ==============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    
    # Add user to database
    add_user(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "",
        last_name=user.last_name or ""
    )
    
    welcome_text = (
        f"👋 Привет, {user.first_name or 'друг'}!\n\n"
        f"🎓 *EduBot* — твой помощник в обучении программированию.\n\n"
        f"Я помогу тебе:\n"
        f"• 📚 Изучить выбранное направление по структурированному плану\n"
        f"• ⏰ Получать напоминания о занятиях\n"
        f"• 📊 Отслеживать прогресс\n"
        f"• 🎯 Дойти до конца и получить поздравление!\n\n"
        f"Выбери действие:"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(user.id)
    )


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu."""
    query = update.callback_query
    await query.answer()
    
    user = get_user(update.effective_user.id)
    
    if not user or not user.get("selected_track"):
        text = "🚀 *Выбери направление обучения:*"
    else:
        track_name = get_track_display_name(user["selected_track"])
        text = f"📚 *Текущее направление:* {track_name}\n\nВыбери действие:"
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(update.effective_user.id)
    )


# ============== Track Selection ==============

async def select_track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show track selection."""
    query = update.callback_query
    await query.answer()
    
    tracks = get_all_tracks()
    
    buttons = []
    for track in tracks:
        display = get_track_display_name(track)
        buttons.append([InlineKeyboardButton(display, callback_data=f"track|{track}")])
    
    buttons.append([InlineKeyboardButton("❌ Отмена", callback_data="main_menu")])
    
    await query.edit_message_text(
        "🚀 *Выбери направление обучения:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def handle_track_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle track selection."""
    query = update.callback_query
    await query.answer()
    
    track = query.data.split("|")[1]
    user_id = update.effective_user.id
    
    # Set user's track
    set_user_track(user_id, track)
    update_user_progress(user_id, stage=1, topic=1)
    
    track_name = get_track_display_name(track)
    
    await query.edit_message_text(
        f"✅ *Направление выбрано:* {track_name}\n\n"
        f"Начнём с первой темы!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Начать обучение", callback_data="continue_learning")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
        ])
    )


# ============== Learning Flow ==============

async def continue_learning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current topic."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user or not user.get("selected_track"):
        await query.edit_message_text(
            "❌ Сначала выбери направление обучения",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Выбрать направление", callback_data="select_track")]
            ])
        )
        return
    
    track = user["selected_track"]
    stage = user.get("current_stage", 1)
    topic_num = user.get("current_topic", 1)
    
    roadmap = parse_roadmap(track)
    if not roadmap:
        await query.edit_message_text("❌ Ошибка загрузки курса")
        return
    
    # Find current topic
    current_topic = None
    total_in_stage = 0
    current_stage_obj = None
    
    for s in roadmap.stages:
        if s.number == stage:
            current_stage_obj = s
            total_in_stage = len(s.topics)
            for t in s.topics:
                if t.topic_num == topic_num:
                    current_topic = t
                    break
    
    if not current_topic:
        await query.edit_message_text("❌ Тема не найдена")
        return
    
    update_last_active(user_id)
    
    # Check if this is the last topic
    is_last_topic = (
        stage == len(roadmap.stages) and 
        topic_num == total_in_stage
    )
    
    text = format_topic_for_display(current_topic, total_in_stage)
    
    if is_last_topic:
        text += "\n🎉 *Это финальная тема!* Заверши курс!"
    
    # Truncate if too long for Telegram (4096 limit)
    if len(text) > 4000:
        text = text[:3950] + "\n\n... *(текст обрезан)*"
    
    try:
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=get_topic_keyboard(track, stage, topic_num, is_last_topic)
            # Web preview enabled for YouTube video previews
        )
    except Exception as e:
        logger.error(f"Error sending topic: {e}")
        await query.edit_message_text(
            "❌ Ошибка загрузки темы. Попробуй ещё раз.",
            reply_markup=get_main_menu_keyboard(user_id)
        )


async def complete_topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark topic as complete and move to next."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("|")
    track = parts[1]
    stage = int(parts[2])
    topic_num = int(parts[3])
    
    user_id = update.effective_user.id
    
    # Mark as completed
    complete_topic(user_id, track, stage, topic_num)
    
    # Get roadmap to find next topic
    roadmap = parse_roadmap(track)
    if not roadmap:
        await query.edit_message_text("❌ Ошибка")
        return
    
    # Find current stage and next topic
    current_stage = None
    for s in roadmap.stages:
        if s.number == stage:
            current_stage = s
            break
    
    if not current_stage:
        await query.edit_message_text("❌ Ошибка")
        return
    
    # Check if there's next topic in current stage
    next_topic = None
    for t in current_stage.topics:
        if t.topic_num == topic_num + 1:
            next_topic = t
            break
    
    if next_topic:
        # Move to next topic in same stage
        update_user_progress(user_id, stage, topic_num + 1)
        await query.edit_message_text(
            f"✅ Тема пройдена!\n\nПереходим к следующей...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Продолжить", callback_data="continue_learning")]
            ])
        )
    else:
        # Check if there's next stage
        next_stage = None
        for s in roadmap.stages:
            if s.number == stage + 1:
                next_stage = s
                break
        
        if next_stage and next_stage.topics:
            # Move to first topic of next stage
            update_user_progress(user_id, stage + 1, 1)
            await query.edit_message_text(
                f"🎉 *Этап {stage} завершён!*\n\n"
                f"Начинаем этап {stage + 1}: {next_stage.name}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📚 Продолжить", callback_data="continue_learning")]
                ])
            )
        else:
            # Course completed!
            await query.edit_message_text(
                f"🎉🎉🎉 *Поздравляем!* 🎉🎉🎉\n\n"
                f"Ты завершил курс *{get_track_display_name(track)}*!\n\n"
                f"Это большое достижение! Теперь ты можешь:\n"
                f"• Начать новый курс\n"
                f"• Применить знания на практике\n"
                f"• Углубиться в изученные темы\n\n"
                f"Продолжай в том же духе! 💪",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 Новый курс", callback_data="select_track")],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
                ])
            )


# ============== Progress ==============

async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user progress."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user or not user.get("selected_track"):
        await query.edit_message_text(
            "❌ Сначала выбери направление",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Выбрать направление", callback_data="select_track")]
            ])
        )
        return
    
    track = user["selected_track"]
    stage = user.get("current_stage", 1)
    topic_num = user.get("current_topic", 1)
    
    roadmap = parse_roadmap(track)
    if not roadmap:
        await query.edit_message_text("❌ Ошибка")
        return
    
    # Get completion stats
    stats = get_completion_stats(user_id, track, roadmap.total_topics)
    
    # Get current topic name
    current_topic_name = "Неизвестно"
    for s in roadmap.stages:
        if s.number == stage:
            for t in s.topics:
                if t.topic_num == topic_num:
                    current_topic_name = t.title
                    break
    
    # Get completed topics
    completed = get_completed_topics(user_id, track)
    
    text = (
        f"📊 *Твой прогресс*\n\n"
        f"🎯 *Курс:* {get_track_display_name(track)}\n"
        f"📍 *Текущая тема:* {current_topic_name}\n"
        f"📈 *Пройдено:* {stats['completed']} из {stats['total']} ({stats['percentage']}%)\n\n"
    )
    
    if completed:
        text += "✅ *Завершённые темы:*\n"
        for c in completed[-10:]:  # Show last 10
            text += f"  • Этап {c['stage']}, тема {c['topic']}\n"
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(user_id)
    )


# ============== Reminders ==============

async def setup_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start reminder setup flow."""
    query = update.callback_query
    await query.answer()
    
    user = get_user(update.effective_user.id)
    if not user or not user.get("selected_track"):
        await query.edit_message_text(
            "❌ Сначала выбери направление",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Выбрать", callback_data="select_track")]
            ])
        )
        return ConversationHandler.END
    
    # Show current reminders
    reminders = get_active_reminders(update.effective_user.id)
    
    text = "⏰ *Настройка напоминаний*\n\n"
    
    if reminders:
        text += "*Активные напоминания:*\n"
        for r in reminders:
            days_str = format_days_display(r["schedule_type"], r["days"])
            text += f"• {days_str} в {r['time']}\n"
        text += "\n"
    
    text += "Выбери, когда присылать напоминания:"
    
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=get_schedule_type_keyboard()
    )
    
    return SELECTING_SCHEDULE_TYPE


async def handle_schedule_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle schedule type selection."""
    query = update.callback_query
    await query.answer()
    
    schedule_type = query.data.split("|")[1]
    context.user_data["schedule_type"] = schedule_type
    
    if schedule_type == "custom":
        context.user_data["selected_days"] = []
        await query.edit_message_text(
            "⚙️ *Выбери дни недели:*\n\n"
            "Нажми на день, чтобы выбрать/отменить",
            parse_mode="Markdown",
            reply_markup=get_days_keyboard()
        )
        return SELECTING_DAYS
    else:
        await query.edit_message_text(
            "🕐 *Выбери время:*\n\n"
            "Когда присылать напоминания?",
            parse_mode="Markdown",
            reply_markup=get_time_keyboard()
        )
        return SELECTING_TIME


async def handle_day_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle day toggle in custom schedule."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "days_done":
        if not context.user_data.get("selected_days"):
            await query.answer("⚠️ Выбери хотя бы один день!")
            return SELECTING_DAYS
        
        await query.edit_message_text(
            "🕐 *Выбери время:*\n\n"
            "Когда присылать напоминания?",
            parse_mode="Markdown",
            reply_markup=get_time_keyboard()
        )
        return SELECTING_TIME
    
    day = query.data.split("|")[1]
    selected = context.user_data.get("selected_days", [])
    
    if day in selected:
        selected.remove(day)
    else:
        selected.append(day)
    
    context.user_data["selected_days"] = selected
    
    await query.edit_message_text(
        "⚙️ *Выбери дни недели:*\n\n"
        f"Выбрано: {', '.join(selected) if selected else 'ничего'}",
        parse_mode="Markdown",
        reply_markup=get_days_keyboard(selected)
    )
    return SELECTING_DAYS


async def handle_time_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle time selection and save reminder."""
    query = update.callback_query
    await query.answer()
    
    time = query.data.split("|")[1]
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    schedule_type = context.user_data.get("schedule_type", "weekdays")
    days = context.user_data.get("selected_days", [])
    track = user["selected_track"]
    
    # Save reminder
    add_reminder(user_id, track, schedule_type, days, time)
    
    days_str = format_days_display(schedule_type, days)
    
    await query.edit_message_text(
        f"✅ *Напоминание настроено!*\n\n"
        f"📚 Курс: {get_track_display_name(track)}\n"
        f"📅 Расписание: {days_str}\n"
        f"🕐 Время: {time}\n\n"
        f"Буду напоминать о занятиях! 🎯",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(user_id)
    )
    
    return ConversationHandler.END


async def cancel_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel reminder setup."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "❌ Настройка отменена",
        reply_markup=get_main_menu_keyboard(update.effective_user.id)
    )
    return ConversationHandler.END


# ============== Error Handler ==============

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error: {context.error}")
    
    if update and update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                "❌ Произошла ошибка. Попробуй позже.",
                reply_markup=get_main_menu_keyboard(update.effective_user.id)
            )
        except:
            pass


# ============== Main ==============

def main():
    """Start the bot."""
    # Init database
    init_db()
    
    # Get token
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ Укажи BOT_TOKEN в переменных окружения")
        sys.exit(1)
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Start reminder scheduler
    async def send_message(user_id: int, text: str):
        await application.bot.send_message(
            user_id, 
            text, 
            parse_mode="Markdown"
            # Web preview enabled for YouTube video previews in reminders
        )
    
    start_scheduler(send_message)
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    
    # Reminder setup conversation
    reminder_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(setup_reminders, pattern="^setup_reminders$")],
        states={
            SELECTING_SCHEDULE_TYPE: [
                CallbackQueryHandler(handle_schedule_type, pattern="^stype\|"),
                CallbackQueryHandler(cancel_setup, pattern="^main_menu$")
            ],
            SELECTING_DAYS: [
                CallbackQueryHandler(handle_day_selection, pattern="^(day\||days_done$)"),
                CallbackQueryHandler(cancel_setup, pattern="^main_menu$")
            ],
            SELECTING_TIME: [
                CallbackQueryHandler(handle_time_selection, pattern="^time\|"),
                CallbackQueryHandler(cancel_setup, pattern="^main_menu$")
            ]
        },
        fallbacks=[CallbackQueryHandler(cancel_setup, pattern="^main_menu$")]
    )
    application.add_handler(reminder_conv)
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(select_track, pattern="^select_track$"))
    application.add_handler(CallbackQueryHandler(handle_track_selection, pattern="^track\|"))
    application.add_handler(CallbackQueryHandler(continue_learning, pattern="^continue_learning$"))
    application.add_handler(CallbackQueryHandler(complete_topic_handler, pattern="^complete\|"))
    application.add_handler(CallbackQueryHandler(show_progress, pattern="^show_progress$"))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Run
    print("🤖 Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
