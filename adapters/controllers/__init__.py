"""
Контроллеры - REST API адаптеры.
Содержит HTTP-роутеры для игроков, игр, результатов и лидерборда.
"""

from adapters.controllers.player_controller import router as player_router
from adapters.controllers.game_controller import router as game_router
from adapters.controllers.score_controller import router as score_router
from adapters.controllers.leaderboard_controller import router as leaderboard_router

__all__ = [
    'player_router',
    'game_router',
    'score_router',
    'leaderboard_router'
]