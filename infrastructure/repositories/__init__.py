"""
Репозитории - слой доступа к данным.
Содержит реализации репозиториев для работы с БД.
"""

from infrastructure.repositories.player_repository import PlayerRepository, PlayerRepositoryProtocol
from infrastructure.repositories.game_repository import GameRepository, GameRepositoryProtocol
from infrastructure.repositories.score_repository import ScoreRepository, ScoreRepositoryProtocol

__all__ = [
    'PlayerRepository',
    'PlayerRepositoryProtocol',
    'GameRepository',
    'GameRepositoryProtocol',
    'ScoreRepository',
    'ScoreRepositoryProtocol'
]