# EduBot

Telegram бот для структурированного обучения с напоминаниями и отслеживанием прогресса.

## 📚 Документация

- [README.md](README.md) — Общее описание
- [STRUCTURE.md](STRUCTURE.md) — Архитектура проекта
- [DEPLOY.md](DEPLOY.md) — Инструкции по деплою

## 🚀 Быстрый старт

```bash
# Установка
pip install -r requirements.txt

# Настройка
cp .env.example .env
# Отредактируй .env, добавь BOT_TOKEN

# Запуск
python src/bot.py
```

## 🐳 Docker

```bash
# Сборка и запуск
docker-compose up -d

# Логи
docker-compose logs -f

# Остановка
docker-compose down
```

## 📁 Структура

```
edu-bot/
├── src/           # Исходный код
├── roadmaps/      # Markdown-курсы
├── data/          # SQLite база данных
├── Dockerfile     # Docker образ
└── docker-compose.yml
```

## 🎓 Курсы

- 🚀 Go Backend
- 🐍 Python Backend  
- ⚡ JavaScript Frontend

## ⚙️ Команды бота

- `/start` — Начало, выбор направления
- 📚 Продолжить обучение
- 📊 Мой прогресс
- ⏰ Настроить напоминания

---

Создано с ❤️ для обучения программированию.
