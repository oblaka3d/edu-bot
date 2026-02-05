# 🚀 Go Backend Roadmap

> Backend разработка на Go — от основ до production-ready сервисов
> Длительность: 6–8 месяцев

---

## Этап 1: Основы Go

**Длительность:** 3 недели

### Тема 1.1: Установка и окружение
- Установка Go (golang.org/dl)
- Настройка GOPATH, GOROOT
- IDE: VS Code + Go extension
- `go mod init` — инициализация модуля
- Структура проекта

**Практика:**
- Настройка рабочего окружения
- Создание первого модуля

**Ресурсы:**
- [A Tour of Go](https://go.dev/tour)
- [Go by Example](https://gobyexample.com/)

---

### Тема 1.2: Базовый синтаксис
- Переменные, типы данных
- Константы и iota
- Функции, возвращаемые значения
- Кортежи (multiple returns)

**Практика:**
- CLI-калькулятор с базовыми операциями

**Видео:**
- [Golang за 100 минут](https://www.youtube.com/watch?v=8dS7aT-s_H0)

---

### Тема 1.3: Управляющие конструкции
- if/else, switch
- for, range
- break, continue

**Практика:**
- Игра "Угадай число"
- Таблица умножения

---

### Тема 1.4: Структуры данных
- Массивы и срезы (slices)
- Карты (maps)
- Структуры (structs)

**Практика:**
- Телефонная книга (структуры + срезы)

---

### Тема 1.5: Работа с ошибками
- Тип error
- Создание ошибок
- Обработка ошибок (if err != nil)
- defer/panic/recover

**Практика:**
- Функция деления с обработкой ошибок

---

## Этап 2: Concurrency

**Длительность:** 1.5–2 месяца

### Тема 2.1: Goroutines
- Что такое goroutine
- Запуск параллельных задач
- runtime.GOMAXPROCS

**Практика:**
- Параллельная обработка URL

---

### Тема 2.2: Каналы (Channels)
- Buffered и unbuffered каналы
- Запись и чтение
- Закрытие каналов
- range по каналу

**Практика:**
- Worker pool для обработки задач

---

### Тема 2.3: Select
- Мультиплексирование каналов
- timeout с select
- default case

**Практика:**
- Скоростной загрузчик с таймаутом

---

### Тема 2.4: Синхронизация
- sync.WaitGroup
- sync.Mutex
- sync.RWMutex
- sync.Once

**Практика:**
- Потокобезопасный счётчик

---

### Тема 2.5: Context
- context.Background, context.TODO
- WithCancel, WithTimeout
- Передача context через функции

**Практика:**
- HTTP клиент с отменой запроса

---

## Этап 3: HTTP и Web

**Длительность:** 2–3 недели

### Тема 3.1: net/http основы
- http.Server, http.Handler
- http.HandleFunc
- http.ListenAndServe

**Практика:**
- Простой сервер с echo

---

### Тема 3.2: Маршрутизация
- Стандартный mux
- URL параметры
- Query parameters

**Практика:**
- REST API для TODO-листа (без БД)

---

### Тема 3.3: Middleware
- Паттерн middleware
- Логирование запросов
- Recovery от паник

**Практика:**
- Сервис с логированием и recovery

---

### Тема 3.4: Работа с JSON
- json.Marshal/Unmarshal
- Структуры с тегами
- json.Encoder

**Практика:**
- API с JSON ответами

---

## Этап 4: Базы данных

**Длительность:** 2–3 недели

### Тема 4.1: SQL основы
- database/sql
- Подключение к PostgreSQL
- Выполнение запросов
- Подготовленные выражения

**Практика:**
- CRUD для пользователей

---

### Тема 4.2: GORM
- Установка и настройка
- Модели и миграции
- CRUD операции
- Связи (has-one, has-many, many-to-many)

**Практика:**
- API с GORM для блога

---

### Тема 4.3: Миграции
- golang-migrate
- Версионирование схемы
- Rollback миграций

**Практика:**
- Миграции для production проекта

---

## Этап 5: REST API Production

**Длительность:** 3–4 недели

### Тема 5.1: Архитектура API
- Структура проекта (Clean Architecture)
- Handlers, Services, Repositories
- DI (Dependency Injection)

**Практика:**
- Рефакторинг TODO API по слоям

---

### Тема 5.2: Аутентификация
- JWT токены
- Middleware для авторизации
- Регистрация и логин

**Практика:**
- API с JWT авторизацией

---

### Тема 5.3: Валидация
- validator.v10
- Валидация входных данных
- Обработка ошибок валидации

**Практика:**
- API с валидацией запросов

---

### Тема 5.4: Тестирование
- Unit tests (testing)
- Table-driven tests
- HTTP тесты (httptest)
- Mock'и

**Практика:**
- Покрытие тестами API

---

## Этап 6: Deploy и DevOps

**Длительность:** 1–2 месяца

### Тема 6.1: Docker
- Dockerfile для Go
- Multi-stage builds
- docker-compose

**Практика:**
- Контейнеризация API

---

### Тема 6.2: CI/CD
- GitHub Actions
- Автотесты
- Сборка и публикация образов

**Практика:**
- Настройка CI/CD для проекта

---

### Тема 6.3: Deploy
- Развёртывание на VPS
- systemd сервисы
- nginx reverse proxy
- SSL (Let's Encrypt)

**Практика:**
- Деплой API на сервер

---

## 🎓 Финальный проект

Создай production-ready сервис:
- REST API с авторизацией
- База данных PostgreSQL
- Docker + CI/CD
- Deploy на VPS

**Примеры:**
- URL shortener
- Сервис заметок
- API для магазина
