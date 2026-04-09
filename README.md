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
├── pytest.ini                        # Конфигурация pytest
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
│   ├── game_use_cases.py
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
├── static/
│   └── index.html                    # Клиентский интерфейс
│
└── tests/                           # Тесты
    ├── conftest.py                   # Pytest фикстуры
    ├── entities/                    # Тесты сущностей
    │   ├── test_player.py
    │   ├── test_game.py
    │   └── test_score.py
    ├── use_cases/                   # Тесты бизнес-логики
    │   ├── test_player_use_cases.py
    │   ├── test_game_use_cases.py
    │   ├── test_score_use_cases.py
    │   └── test_leaderboard_use_cases.py
    ├── adapters/controllers/         # Тесты API
    │   ├── test_player_controller.py
    │   ├── test_game_controller.py
    │   ├── test_score_controller.py
    │   └── test_leaderboard_controller.py
    └── infrastructure/               # Тесты инфраструктуры
        ├── test_database.py
        ├── test_startup.py
        └── repositories/
            ├── test_player_repository.py
            ├── test_game_repository.py
            └── test_score_repository.py
```

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/asterix1221/leaderboard
cd kursach5
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

## Тестирование

Проект включает комплексный набор тестов, покрывающих все слои приложения:

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием кода
pytest --cov=. --cov-report=html

# Запуск определённой группы тестов
pytest tests/entities/          # Тесты сущностей
pytest tests/use_cases/          # Тесты бизнес-логики
pytest tests/adapters/           # Тесты API
pytest tests/infrastructure/      # Тесты инфраструктуры
```

### Тестовые маркеры

- `unit` — Юнит-тесты (изолированные, без внешних зависимостей)
- `integration` — Интеграционные тесты (с базой данных)
- `api` — API тесты (HTTP эндпоинты)

### Структура тестов

Тесты организованы по слоям архитектуры:

| Уровень | Директория | Описание |
|---------|------------|-----------|
| Entities | `tests/entities/` | Тесты бизнес-сущностей (Player, Game, Score) |
| Use Cases | `tests/use_cases/` | Тесты бизнес-логики |
| Adapters | `tests/adapters/controllers/` | Тесты REST API контроллеров |
| Infrastructure | `tests/infrastructure/` | Тесты репозиториев и базы данных |

### Конфигурация

- **conftest.py** — Общие фикстуры для всех тестов
- **pytest.ini** — Конфигурация pytest с маркерами и путями
