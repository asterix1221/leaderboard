# Game Leaderboard System

Серверная часть системы лидербордов для игры на Python с использованием FastAPI и Clean Architecture.

## Описание

Веб-приложение предоставляет REST API для управления игроками, играми, результатами и таблицами лидеров. Клиентская часть реализована как SPA на Vanilla JS с тёмной темой.

## Архитектура

Проект построен на принципах **Clean Architecture** с четырьмя слоями:

1. **Entities** (Сущности) — бизнес-объекты, не зависящие от фреймворков
2. **Use Cases** (Сценарии использования) — бизнес-логика приложения
3. **Adapters** (Адаптеры интерфейсов) — REST контроллеры и Pydantic-схемы
4. **Infrastructure** (Инфраструктура) — SQLAlchemy модели и репозитории

## Технологический стек

- **Backend**: Python 3.11+ / FastAPI
- **ORM**: SQLAlchemy 2.0
- **База данных**: SQLite (файл `leaderboard.db`)
- **Валидация**: Pydantic v2
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Сервер**: Uvicorn

## Структура проекта

```
leaderboard/
├── main.py                           # Точка входа
├── requirements.txt                  # Зависимости
├── leaderboard.db                    # SQLite база данных
│
├── entities/                         # Бизнес-сущности
│   ├── player.py                    # Игрок
│   ├── score.py                     # Результат
│   └── game.py                      # Игра
│
├── use_cases/                       # Сценарии использования
│   ├── player_use_cases.py
│   ├── score_use_cases.py
│   └── leaderboard_use_cases.py
│
├── adapters/                        # Адаптеры
│   ├── controllers/                 # REST API
│   │   ├── player_controller.py
│   │   ├── score_controller.py
│   │   ├── game_controller.py
│   │   └── leaderboard_controller.py
│   └── schemas/                     # Pydantic модели
│
├── infrastructure/                   # Инфраструктура
│   ├── database.py                  # Подключение к БД
│   ├── models/                       # SQLAlchemy модели
│   └── repositories/                 # CRUD операции
│
└── static/
    └── index.html                    # Клиентский интерфейс
```

## Установка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd leaderboard
```

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

Запуск сервера:

```bash
uvicorn main:app --reload --port 8000
```

Или через Python:

```bash
python main.py
```

Приложение будет доступно по адресу: **<http://localhost:8000>**

## REST API

### Игроки

- `POST /api/players` — Регистрация нового игрока
- `GET /api/players/{id}` — Получение профиля игрока

### Игры

- `POST /api/games` — Создание новой игры
- `GET /api/games` — Получение списка всех игр

### Результаты

- `POST /api/scores` — Отправка результата игры
- `GET /api/scores/player/{player_id}` — Получение всех результатов игрока

### Лидерборд

- `GET /api/leaderboard/{game_id}` — Получение топ-10 игроков для игры
- `GET /api/leaderboard/{game_id}?limit=N` — Получение топ-N игроков

## Тестовые данные

При первом запуске автоматически создаются:

- 3 игры: "Space Shooter", "Puzzle Master", "Racing Pro"
- 5 игроков: player1–player5
- Случайные результаты для демонстрации лидерборда

## Клиентский интерфейс

Веб-интерфейс доступен по адресу `/static/index.html` и включает:

- **Лидерборд** — просмотр таблицы лидеров с выбором игры
- **Отправить результат** — форма для отправки новых результатов
- **Регистрация игрока** — создание новых игроков
- **Управление играми** — добавление и просмотр игр

## Требования к коду

- Все комментарии на русском языке
- Каждый файл начинается с описания назначения
- Соблюдение зависимостей Clean Architecture
- Использование dependency injection

## Примеры использования API

### Регистрация игрока

```bash
curl -X POST http://localhost:8000/api/players \
  -H "Content-Type: application/json" \
  -d '{"username": "new_player"}'
```

### Отправка результата

```bash
curl -X POST http://localhost:8000/api/scores \
  -H "Content-Type: application/json" \
  -d '{"player_id": 1, "game_id": 1, "value": 5000}'
```

### Получение лидерборда

```bash
curl http://localhost:8000/api/leaderboard/1
```

## Лицензия

MIT License
