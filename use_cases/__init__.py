"""
Сценарии использования (Use Cases) - бизнес-логика приложения.
Содержит сценарии для работы с игроками, результатами и лидербордом.
"""

from use_cases.player_use_cases import PlayerUseCases
from use_cases.score_use_cases import ScoreUseCases
from use_cases.leaderboard_use_cases import LeaderboardUseCases, LeaderboardEntry
from use_cases.game_use_cases import GameUseCases

__all__ = [
    'PlayerUseCases',
    'ScoreUseCases',
    'LeaderboardUseCases',
    'LeaderboardEntry',
    'GameUseCases'
]