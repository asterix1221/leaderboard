"""
Сценарии использования для работы с лидербордом.
Содержит бизнес-логику получения таблицы лидеров.
"""

from dataclasses import dataclass
from infrastructure.repositories import ScoreRepositoryProtocol, GameRepositoryProtocol


@dataclass
class LeaderboardEntry:
    """
    Запись в таблице лидеров.
    """
    rank: int
    player_id: int
    username: str
    value: int
    achieved_at: str


class LeaderboardUseCases:
    """
    Сценарии использования для работы с лидербордом.
    Реализует бизнес-логику формирования рейтинга игроков.
    """
    
    def __init__(
        self,
        score_repo: ScoreRepositoryProtocol,
        game_repo: GameRepositoryProtocol
    ):
        """
        Инициализация сценариев использования.
        
        Args:
            score_repo: Репозиторий результатов
            game_repo: Репозиторий игр
        """
        self.score_repo = score_repo
        self.game_repo = game_repo
    
    def get_leaderboard(self, game_id: int, limit: int = 10) -> list[LeaderboardEntry]:
        """
        Получить топ-N игроков по наилучшему результату в указанной игре.
        
        Для каждого игрока возвращается только лучший результат.
        
        Args:
            game_id: Идентификатор игры
            limit: Количество позиций в таблице лидеров (по умолчанию 10)
            
        Returns:
            Список записей лидерборда с рангом, именем и очками
            
        Raises:
            ValueError: Если игра не найдена
        """
        # Проверка существования игры
        game = self.game_repo.find_by_id(game_id)
        if not game:
            raise ValueError("Игра не найдена")
        
        # Получаем лучшие результаты из репозитория
        raw_scores = self.score_repo.get_top_scores(game_id, limit)
        
        # Добавляем ранг к каждой записи
        return [
            LeaderboardEntry(
                rank=i + 1,
                player_id=entry["player_id"],
                username=entry["username"],
                value=entry["value"],
                achieved_at=entry["achieved_at"].isoformat() if entry["achieved_at"] else ""
            )
            for i, entry in enumerate(raw_scores)
        ]