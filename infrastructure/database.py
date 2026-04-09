"""
Модуль базы данных - настройка подключения к SQLite.
Содержит движок SQLAlchemy, создание таблиц и сессию для работы с БД.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Путь к файлу базы данных
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "leaderboard.db"

# Строка подключения к SQLite
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Создание движка SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # False - не выводить SQL-запросы в консоль
    connect_args={"check_same_thread": False}  # Разрешить многопоточный доступ
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """
    Генератор сессии базы данных.
    Используется для dependency injection в FastAPI.
    
    Yields:
        Сессия SQLAlchemy для работы с БД
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Создание всех таблиц в базе данных.
    Вызывается при старте приложения.
    """
    from infrastructure.models.player_model import PlayerModel
    from infrastructure.models.game_model import GameModel
    from infrastructure.models.score_model import ScoreModel
    
    Base.metadata.create_all(bind=engine)