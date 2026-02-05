# 🐘 Настройка PostgreSQL на Railway

## Шаг 1: Создать базу данных

1. В Railway проекте нажми **New** или **Add**
2. Выбери **Database** → **Add PostgreSQL**
3. Дождись создания (статус: "Running")

## Шаг 2: Подключить к сервису

1. Кликни на сервис с ботом (edu-bot)
2. Перейди во вкладку **Variables**
3. Нажми **New Variable**
4. Выбери **Add Reference** → выбери PostgreSQL
5. Railway автоматически добавит `DATABASE_URL`

Или вручную:
• Кликни на PostgreSQL
• Перейди во вкладку **Connect**
• Скопируй **Database URL**
• Добавь в Variables сервиса бота как `DATABASE_URL`

## Шаг 3: Перезапустить

1. Railway автоматически перезапустит бота
2. В логах увидишь: "🐘 Using PostgreSQL database"

## Готово! 🎉

Теперь все данные сохраняются в PostgreSQL и не пропадут при redeploy.

---

## Проверка

Отправь боту `/start` — он должен работать как обычно.

Если в логах: "🗄️ Using SQLite database" — значит DATABASE_URL не подхватился, проверь переменные.
