<p align="center">
  <img src="assets/001-skilltree-logo-digital-tree-made-of-glow.png" alt="SkillTree Logo" width="200"/>
</p>

<h1 align="center">🌳 SkillTree</h1>

<p align="center">
  Telegram бот для структурированного обучения с напоминаниями и отслеживанием прогресса
</p>

<p align="center">
  <a href="#-быстрый-старт">Быстрый старт</a> •
  <a href="#-документация">Документация</a> •
  <a href="#-деплой">Деплой</a>
</p>

---

## ✨ Возможности

- 📚 **Структурированные курсы** — Go, Python, JavaScript
- ⏰ **Умные напоминания** — будни, выходные, произвольные дни
- 📊 **Отслеживание прогресса** — текущая тема, % завершения
- 🎯 **Прокачка навыков** — как в RPG: проходи темы, получай прогресс
- 🎉 **Поздравления** — при завершении курса

## 🚀 Быстрый старт

```bash
# Клонирование
git clone https://github.com/oblaka3d/edu-bot.git skilltree
cd skilltree

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

## 📚 Документация

- [STRUCTURE.md](STRUCTURE.md) — Архитектура проекта
- [DEPLOY.md](DEPLOY.md) — Инструкции по деплою
- [RAILWAY.md](RAILWAY.md) — Деплой на Railway

## 📁 Структура

```
skilltree/
├── src/           # Исходный код
├── roadmaps/      # Markdown-курсы
├── assets/        # Логотипы и изображения
├── data/          # SQLite база данных
├── Dockerfile     # Docker образ
└── docker-compose.yml
```

## 🎓 Курсы

| Курс | Этапов | Тем |
|------|--------|-----|
| 🚀 Go Backend | 6 | ~25 |
| 🐍 Python Backend | 6 | ~24 |
| ⚡ JavaScript Frontend | 6 | ~25 |

## ⚙️ Команды бота

- `/start` — Начало, выбор направления
- 📚 **Продолжить обучение** — текущая тема с материалами
- 📊 **Мой прогресс** — статистика и история
- ⏰ **Настроить напоминания** — расписание занятий

## 🚂 Деплой

### Railway (рекомендуется)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template?template=https://github.com/oblaka3d/edu-bot)

Или вручную: см. [RAILWAY.md](RAILWAY.md)

## 📝 Добавление курса

Просто создай `roadmaps/мой-курс.md` по формату:

```markdown
# Название курса

## Этап 1: Название

### Тема 1.1: Тема
📖 **Изучим:**
• Пункт 1

🎥 **Видео:**
• [Название](https://youtube.com/...)

💻 **Практика:**
• Задание
```

Курс автоматически появится в выборе!

---

<p align="center">
  Создано с ❤️ для обучения программированию
</p>
