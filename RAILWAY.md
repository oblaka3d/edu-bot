# 🚂 Деплой на Railway (пошаговая инструкция)

## 1. Подготовка

```bash
cd /home/hithere/clawd/projects/edu-bot

# Инициализируем git (если ещё нет)
git init
git add .
git commit -m "Initial commit"
```

## 2. Создай репозиторий на GitHub

```bash
# Создай репозиторий на https://github.com/new
# Название: edu-bot (или любое)
# Public или Private — не важно

# Привяжи и запушь
git remote add origin https://github.com/ТВОЙ_USERNAME/edu-bot.git
git branch -M main
git push -u origin main
```

## 3. Railway

### 3.1 Регистрация
- Зайди на https://railway.app
- Войди через GitHub

### 3.2 Создай проект
- **New Project**
- **Deploy from GitHub repo**
- Выбери свой `edu-bot` репозиторий

### 3.3 Добавь переменные
- Перейди в **Variables**
- Добавь:
  - `BOT_TOKEN` = твой токен от @BotFather
  - `TZ` = Europe/Moscow

### 3.4 Добавь Volume (для данных)
- Перейди в **Settings** → **Volumes**
- Add Volume:
  - Mount Path: `/app/data`
  - Size: 1GB

### 3.5 Деплой
- Railway автоматически задеплоит
- Статус: **Deploying...** → **Success**

## 4. Проверка

1. Отправь `/start` своему боту
2. Должно прийти приветственное сообщение

## 5. Настройка домена (опционально)

Railway даёт случайный домен. Если нужен вебхук (для групп):
- **Settings** → **Domains**
- Добавь свой или используй случайный

## 🔄 Обновление бота

```bash
# Внеси изменения локально
git add .
git commit -m "Обновление"
git push

# Railway автоматически перезадеплоит!
```

## 📊 Мониторинг

- Логи: вкладка **Logs** в Railway
- Метрики: вкладка **Metrics**
- Перезапуск: кнопка **Redeploy**

## ❓ Проблемы

**Бот не отвечает:**
- Проверь `BOT_TOKEN` в Variables
- Посмотри логи в Railway
- Перезапусти деплой

**Данные сбрасываются:**
- Убедись что Volume `/app/data` добавлен

## 💰 Лимиты бесплатного тарифа

- 500 часов выполнения в месяц (~20 дней непрерывно)
- 1GB RAM
- 1GB диск

💡 Для 24/7 работы: Railway + UptimeRobot (пинг каждые 5 минут)
