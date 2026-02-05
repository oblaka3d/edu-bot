# 🚀 Go Backend Roadmap

> Backend разработка на Go — от основ до production-ready сервисов
> Длительность: 6–8 месяцев

---

## Этап 1: Основы Go

**Длительность:** 3 недели

### Тема 1.1: Установка Go и окружение

📖 **Изучим:**
• Установка Go (golang.org/dl)
• Настройка окружения: GOPATH, GOROOT, GOBIN
• IDE: VS Code + Go extension или GoLand
• `go mod init` — инициализация модуля
• `go get` — установка пакетов
• Структура проекта и рабочего пространства

🎥 **Видео:**
• [Golang за 100 минут](https://www.youtube.com/watch?v=8dS7aT-s_H0)
• [Полный курс Go (8 часов)](https://www.youtube.com/watch?v=SXTQj6XJOWg)

📚 **Ресурсы:**
• [A Tour of Go](https://go.dev/tour) — интерактивный тур
• [Go by Example](https://gobyexample.com/)
• [Документация Go](https://pkg.go.dev/)

💻 **Практика:**
• Настройка рабочего окружения
• Создание первого модуля `hello-world`
• Сборка и запуск программы

---

### Тема 1.2: Базовый синтаксис

📖 **Изучим:**
• Переменные: объявление, типы, краткая форма `:=`
• Типы данных: int, float64, string, bool
• Константы и `iota` для перечислений
• Функции: объявление, параметры, возвращаемые значения
• Кортежи (multiple returns) — возврат нескольких значений
• Анонимные функции

🎥 **Видео:**
• [Основы Go (Артём Шумайлов)](https://www.youtube.com/watch?v=9Tz6C5TVvAM)

📚 **Ресурсы:**
• [Go Types](https://go.dev/tour/basics/11)
• [Effective Go](https://go.dev/doc/effective_go)

💻 **Практика:**
• CLI-калькулятор (+, -, *, /)
• Функция swap для обмена значений
• Конвертер температур (Celsius ↔ Fahrenheit)

---

### Тема 1.3: Управляющие конструкции

📖 **Изучим:**
• Условные операторы: if/else, switch
• Циклы: for (единственный цикл в Go)
• Range: итерация по слайсам, мапам, строкам
• break, continue, labels
• Отложенный вызов: defer

🎥 **Видео:**
• [Control Flow в Go](https://www.youtube.com/watch?v=IXa92OEk5x0)

📚 **Ресурсы:**
• [Go Flow Control](https://go.dev/tour/flowcontrol/1)

💻 **Практика:**
• Игра "Угадай число" (random + циклы)
• Таблица умножения
• FizzBuzz
• Проверка палиндрома

---

### Тема 1.4: Структуры данных

📖 **Изучим:**
• Массивы: фиксированный размер
• Срезы (slices): динамические массивы, append, copy
• Карты (maps): хеш-таблицы, ключ-значение
• Структуры (structs): пользовательские типы
• Вложенные структуры
• Теги структур (struct tags)

🎥 **Видео:**
• [Slices and Maps](https://www.youtube.com/watch?v=YS4e4q9oBaU)

📚 **Ресурсы:**
• [Go Slices](https://go.dev/blog/slices-intro)
• [Go Maps](https://go.dev/blog/maps)

💻 **Практика:**
• Телефонная книга (структура + срез)
• Счётчик слов в тексте (map)
• Реализация стека и очереди
• Сортировка слайса

---

### Тема 1.5: Работа с ошибками

📖 **Изучим:**
• Тип `error` — интерфейс
• Создание ошибок: `errors.New`, `fmt.Errorf`
• Обработка ошибок: паттерн `if err != nil`
• Обертывание ошибок (error wrapping)
• defer/panic/recover — отложенный вызов и восстановление
• Когда использовать panic

🎥 **Видео:**
• [Error Handling в Go](https://www.youtube.com/watch?v=WiLGdja3Dz8)

📚 **Ресурсы:**
• [Error Handling](https://go.dev/blog/error-handling-and-go)
• [Defer, Panic, Recover](https://go.dev/blog/defer-panic-and-recover)

💻 **Практика:**
• Функция деления с обработкой деления на ноль
• Валидация email
• Чтение файла с обработкой ошибок
• Логирование ошибок

---

## Этап 2: Concurrency

**Длительность:** 1.5–2 месяца

### Тема 2.1: Goroutines

📖 **Изучим:**
• Что такое goroutine — легковесные потоки
• Запуск с `go` keyword
• runtime.GOMAXPROCS — количество процессоров
• Планировщик Go
• Главная goroutine и ожидание завершения

🎥 **Видео:**
• [Goroutines explained](https://www.youtube.com/watch?v=LvgVSSpwCT8)

📚 **Ресурсы:**
• [Goroutines](https://go.dev/tour/concurrency/1)

💻 **Практика:**
• Параллельная обработка списка URL
• Конкурентный HTTP клиент
• Загрузка файлов параллельно

---

### Тема 2.2: Каналы (Channels)

📖 **Изучим:**
• Buffered vs unbuffered каналы
• Операции: отправка, получение
• Закрытие каналов: `close(ch)`
• Range по каналу
• Направленные каналы: `chan<-`, `<-chan`
• Select для мультиплексирования
• Таймауты с select
• default case в select

🎥 **Видео:**
• [Channels](https://www.youtube.com/watch?v=KBklhOEttHc)
• [Select](https://www.youtube.com/watch?v=1MX_pIy1XM0)

📚 **Ресурсы:**
• [Channels](https://go.dev/tour/concurrency/2)
• [Select](https://go.dev/tour/concurrency/5)

💻 **Практика:**
• Worker pool для обработки задач
• Паттерн Fan-out/Fan-in
• Rate limiter
• Таймер с отменой

---

### Тема 2.3: Синхронизация

📖 **Изучим:**
• sync.WaitGroup — ожидание группы goroutines
• sync.Mutex — взаимное исключение
• sync.RWMutex — читатели-писатели
• sync.Once — однократная инициализация
• sync.Map — потокобезопасная мапа
• atomic операции

🎥 **Видео:**
• [Sync package](https://www.youtube.com/watch?v=yUWoj6kJqMY)

📚 **Ресурсы:**
• [sync package](https://pkg.go.dev/sync)

💻 **Практика:**
• Потокобезопасный счётчик
• Пул соединений с БД
• Кэш с TTL

---

### Тема 2.4: Context

📖 **Изучим:**
• context.Background, context.TODO
• context.WithCancel — отмена операций
• context.WithTimeout — таймауты
• context.WithDeadline — дедлайны
• context.WithValue — передача значений
• Пробрасывание context через функции
• Graceful shutdown

🎥 **Видео:**
• [Context в Go](https://www.youtube.com/watch?v=kaZOXRqFPDw)

📚 **Ресурсы:**
• [Go Concurrency Patterns: Context](https://go.dev/blog/context)

💻 **Практика:**
• HTTP сервер с graceful shutdown
• Отмена долгих запросов
• Трейсинг запросов через context

---

## Этап 3: HTTP и Web

**Длительность:** 2–3 недели

### Тема 3.1: net/http основы

📖 **Изучим:**
• HTTP сервер: `http.Server`
• Обработчики: `http.Handler`, `http.HandlerFunc`
• Маршрутизация: `http.ServeMux`
• Методы HTTP: GET, POST, PUT, DELETE
• Заголовки запросов и ответов
• Query параметры
• Path параметры

🎥 **Видео:**
• [Building Web Servers](https://www.youtube.com/watch?v=ASBUpRsmSlY)

📚 **Ресурсы:**
• [net/http](https://pkg.go.dev/net/http)

💻 **Практика:**
• Эхо-сервер
• REST API для TODO-листа (in-memory)
• Файловый сервер

---

### Тема 3.2: Middleware

📖 **Изучим:**
• Паттерн middleware/chain of responsibility
• Логирование запросов
• Recovery от паник
• CORS обработка
• Аутентификация
• Rate limiting

🎥 **Видео:**
• [Middleware в Go](https://www.youtube.com/watch?v=QvW7y8qV4x8)

💻 **Практика:**
• Сервис с логированием запросов
• JWT middleware
• CORS middleware

---

### Тема 3.3: JSON и сериализация

📖 **Изучим:**
• json.Marshal / json.Unmarshal
• Структуры с тегами `json:"name,omitempty"`
• json.Decoder / json.Encoder для потоков
• Валидация JSON
• Кастомные marshaler/unmarshaler

🎥 **Видео:**
• [JSON в Go](https://www.youtube.com/watch?v=jbYyJNSLKjw)

💻 **Практика:**
• API с JSON ответами
• Валидация входящих данных
• Парсинг конфигурации из JSON

---

## Этап 4: Базы данных

**Длительность:** 2–3 недели

### Тема 4.1: SQL с database/sql

📖 **Изучим:**
• database/sql — стандартный пакет
• Драйверы: pq (PostgreSQL), go-sqlite3
• Подключение к БД: `sql.Open`
• Connection pool
• Выполнение запросов: Exec, Query, QueryRow
• Подготовленные выражения
• Транзакции

🎥 **Видео:**
• [SQL в Go](https://www.youtube.com/watch?v=BwtRMf0lqNU)

📚 **Ресурсы:**
• [database/sql](https://pkg.go.dev/database/sql)

💻 **Практика:**
• CRUD для пользователей
• Работа с транзакциями
• Паттерн Repository

---

### Тема 4.2: GORM

📖 **Изучим:**
• Установка и настройка GORM
• Модели и теги `gorm:"..."`
• Автомиграции
• CRUD операции: Create, First, Find, Update, Delete
• Предзагрузка (Preload)
• Хуки (Hooks)
• Связи: Has One, Has Many, Many to Many

🎥 **Видео:**
• [GORM Tutorial](https://www.youtube.com/watch?v=5xYNof8FLSA)

📚 **Ресурсы:**
• [GORM Docs](https://gorm.io/docs/)

💻 **Практика:**
• API блога с GORM
• E-commerce модели
• Мягкое удаление (soft delete)

---

### Тема 4.3: Миграции

📖 **Изучим:**
• golang-migrate
• Версионирование схемы
• Up/Down миграции
• Интеграция в CI/CD

🎥 **Видео:**
• [Database Migrations](https://www.youtube.com/watch?v=OUqQ6LdJ-ok)

💻 **Практика:**
• Настройка миграций для проекта
• Миграции в Docker

---

## Этап 5: REST API Production

**Длительность:** 3–4 недели

### Тема 5.1: Архитектура

📖 **Изучим:**
• Clean Architecture / Layered Architecture
• Структура проекта
• Handlers (Controllers)
• Services (Business Logic)
• Repositories (Data Access)
• DI (Dependency Injection)
• Интерфейсы для тестируемости

🎥 **Видео:**
• [Project Structure](https://www.youtube.com/watch?v=d_jMeISqFkQ)

💻 **Практика:**
• Рефакторинг TODO API по слоям
• Интерфейсы для Repository

---

### Тема 5.2: Аутентификация и авторизация

📖 **Изучим:**
• JWT (JSON Web Tokens)
• Access и Refresh токены
• Middleware для авторизации
• Хеширование паролей (bcrypt)
• OAuth 2.0 / OpenID Connect
• Sessions vs JWT

🎥 **Видео:**
• [JWT в Go](https://www.youtube.com/watch?v=9j9X8f3cX0A)

📚 **Ресурсы:**
• [jwt-go](https://github.com/golang-jwt/jwt)

💻 **Практика:**
• Регистрация и логин
• Защищённые endpoints
• Обновление токенов

---

### Тема 5.3: Валидация

📖 **Изучим:**
• go-playground/validator
• Теги валидации: `validate:"required,email,min=3"`
• Кастомные валидаторы
• Валидация на уровне handler
• Сообщения об ошибках

🎥 **Видео:**
• [Validation](https://www.youtube.com/watch?v=QP9qq3kHqQQ)

💻 **Практика:**
• Валидация входящих запросов
• Кастомные ошибки валидации

---

### Тема 5.4: Тестирование

📖 **Изучим:**
• Unit тесты: `testing` пакет
• Table-driven tests
• HTTP тесты: `httptest`
• Mock'и: testify/mock, gomock
• Интеграционные тесты
• Coverage

🎥 **Видео:**
• [Testing в Go](https://www.youtube.com/watch?v=yszygk1a4o4)

📚 **Ресурсы:**
• [Testing](https://go.dev/doc/tutorial/add-a-test)

💻 **Практика:**
• Покрытие тестами handlers
• Mock для Repository
• Интеграционные тесты API

---

## Этап 6: Deploy и DevOps

**Длительность:** 1–2 месяца

### Тема 6.1: Docker

📖 **Изучим:**
• Dockerfile для Go
• Multi-stage builds (уменьшение размера)
• docker-compose
• Сеть в Docker
• Volumes для данных

🎥 **Видео:**
• [Docker для Go](https://www.youtube.com/watch?v=wE7yGH0DNNo)

💻 **Практика:**
• Контейнеризация API
• Docker-compose: app + PostgreSQL
• Минимальный образ (< 20MB)

---

### Тема 6.2: CI/CD

📖 **Изучим:**
• GitHub Actions
• Автоматические тесты
• Сборка и публикация Docker образов
• Линтинг: golangci-lint
• Автодеплой

🎥 **Видео:**
• [CI/CD для Go](https://www.youtube.com/watch?v=dbC-d4OeT7k)

💻 **Практика:**
• Настройка GitHub Actions
• Автотесты на PR
• Публикация в Docker Hub

---

### Тема 6.3: Production Deploy

📖 **Изучим:**
• Развёртывание на VPS
• systemd сервисы
• nginx reverse proxy
• SSL сертификаты (Let's Encrypt)
• Логирование и мониторинг
• Graceful shutdown

🎥 **Видео:**
• [Deploy Go App](https://www.youtube.com/watch?v=Z2zTJDNJYQI)

💻 **Практика:**
• Деплой на DigitalOcean/Hetzner
• Настройка nginx
• HTTPS

---

## 🎓 Финальный проект

Создай production-ready сервис:
- REST API с JWT авторизацией
- PostgreSQL база данных
- GORM или чистый SQL
- Docker + docker-compose
- CI/CD pipeline
- Тесты с покрытием > 60%
- Deploy на VPS или Railway/Render

**Идеи:**
- URL shortener
- Сервис заметок
- API для магазина
- Сервис бронирования
- Task management
