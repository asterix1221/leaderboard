"""
Pydantic-схемы - валидация данных и сериализация ответов API.
"""

from adapters.schemas.player_schema import PlayerCreate, PlayerResponse, PlayerWithScores
from adapters.schemas.score_schema import ScoreCreate, ScoreResponse
from adapters.schemas.game_schema import GameCreate, GameResponse
from adapters.schemas.leaderboard_schema import LeaderboardEntrySchema, LeaderboardResponse

__all__ = [
    'PlayerCreate',
    'PlayerResponse',
    'PlayerWithScores',
    'ScoreCreate',
    'ScoreResponse',
    'GameCreate',
    'GameResponse',
    'LeaderboardEntrySchema',
    'LeaderboardResponse'
]