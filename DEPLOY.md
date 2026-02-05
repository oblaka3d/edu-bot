# 🚀 Деплой EduBot

## Вариант 1: Docker (рекомендуется для VPS/сервера)

### Требования
- Docker + Docker Compose
- VPS с 512MB+ RAM
- Постоянный IP (для вебхуков)

### Шаги

1. **Копируем файлы на сервер:**
```bash
scp -r edu-bot user@your-server:/opt/
```

2. **Настраиваем .env:**
```bash
cd /opt/edu-bot
cp .env.example .env
nano .env  # Вставляем BOT_TOKEN
```

3. **Запускаем:**
```bash
docker-compose up -d
```

4. **Проверяем логи:**
```bash
docker-compose logs -f
```

5. **Обновление бота:**
```bash
cd /opt/edu-bot
git pull  # или скопировать новые файлы
docker-compose down
docker-compose up --build -d
```

---

## Вариант 2: Railway (бесплатный хостинг)

### Шаги

1. **Загружаем на GitHub:**
```bash
# Создай репозиторий и запушь
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/edu-bot.git
git push -u origin main
```

2. **Deploy на Railway:**
- Иди на https://railway.app
- New Project → Deploy from GitHub repo
- Выбери свой репозиторий

3. **Добавь переменные:**
- В Settings → Variables добавь `BOT_TOKEN`

4. **Добавь volume для данных:**
- В Settings → Volumes добавь `/app/data`

Готово! Бот будет работать 24/7 на бесплатном тарифе.

---

## Вариант 3: Render.com

### Шаги

1. **Форк на GitHub** (см. выше)

2. **Создай Web Service на Render:**
- New → Web Service
- Выбери репозиторий

3. **Настройки:**
- Runtime: Docker
- Environment: `BOT_TOKEN` в Environment Variables
- Plan: Free

4. **Добавь Disk:**
- Disks → Add Disk
- Mount Path: `/app/data`
- Size: 1GB

---

## Вариант 4: Дома (Raspberry Pi / старый ноутбук)

### Шаги

1. **Установи Docker:**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

2. **Скопируй файлы и запусти:**
```bash
git clone https://github.com/username/edu-bot.git
cd edu-bot
cp .env.example .env
# Редактируй .env, добавь BOT_TOKEN
docker-compose up -d
```

3. **Автозапуск:**
```bash
# Docker Compose уже настроен с restart: unless-stopped
# Но можно добавить в cron для перезапуска после ребута:
@reboot cd /home/pi/edu-bot && docker-compose up -d
```

---

## Вариант 5: Python напрямую (без Docker)

### Шаги

1. **Установи зависимости:**
```bash
cd edu-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Настрой переменные:**
```bash
export BOT_TOKEN="your_token"
```

3. **Запусти:**
```bash
python src/bot.py
```

4. **Для фона используй systemd или screen/tmux:**
```bash
# Через screen
screen -S edubot
python src/bot.py
# Ctrl+A, D — отключиться

# Подключиться обратно:
screen -r edubot
```

---

## 🔄 Обновление бота

### Docker:
```bash
cd /opt/edu-bot
docker-compose down
git pull  # или замени файлы
docker-compose up --build -d
```

### Python напрямую:
```bash
cd edu-bot
git pull
source venv/bin/activate
pip install -r requirements.txt
# Перезапусти процесс
```

---

## 📋 Чек-лист перед деплоем

- [ ] Создан бот в @BotFather, получен токен
- [ ] BOT_TOKEN добавлен в .env или переменные окружения
- [ ] Проверен локально: `python src/bot.py`
- [ ] Данные (data/) будут сохраняться (volume/disk)
- [ ] Настроен автозапуск (если нужно)

---

## 🔧 Проблемы и решения

**Бот не запускается:**
```bash
# Проверь токен
echo $BOT_TOKEN

# Проверь логи
docker-compose logs
```

**Данные не сохраняются:**
- Убедись что volume `/app/data` примонтирован

**Бот перестал отвечать:**
- Перезапусти: `docker-compose restart`

---

*Рекомендация: Railway — самый простой для начала, VPS — лучший для продакшена.*
