"""
Инфраструктурный слой - работа с базой данных и внешними системами.
Содержит подключение к БД, модели SQLAlchemy и репозитории.
"""

from infrastructure.database import get_db, create_tables, engine, SessionLocal
from infrastructure.models import PlayerModel, GameModel, ScoreModel
from infrastructure.repositories import (
    PlayerRepository,
    PlayerRepositoryProtocol,
    GameRepository,
    GameRepositoryProtocol,
    ScoreRepository,
    ScoreRepositoryProtocol
)

__all__ = [
    'get_db',
    'create_tables',
    'engine',
    'SessionLocal',
    'PlayerModel',
    'GameModel',
    'ScoreModel',
    'PlayerRepository',
    'PlayerRepositoryProtocol',
    'GameRepository',
    'GameRepositoryProtocol',
    'ScoreRepository',
    'ScoreRepositoryProtocol'
]