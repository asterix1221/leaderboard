"""
Сценарии использования для работы с результатами.
Содержит бизнес-логику отправки и получения результатов игр.
"""

from datetime import datetime
from entities.score import Score
from infrastructure.repositories import ScoreRepositoryProtocol, PlayerRepositoryProtocol, GameRepositoryProtocol


class ScoreUseCases:
    """
    Сценарии использования для работы с результатами.
    Реализует бизнес-логику, связанную с результатами игр.
    """
    
    def __init__(
        self,
        score_repo: ScoreRepositoryProtocol,
        player_repo: PlayerRepositoryProtocol,
        game_repo: GameRepositoryProtocol
    ):
        """
        Инициализация сценариев использования.
        
        Args:
            score_repo: Репозиторий результатов
            player_repo: Репозиторий игроков
            game_repo: Репозиторий игр
        """
        self.score_repo = score_repo
        self.player_repo = player_repo
        self.game_repo = game_repo
    
    def submit_score(self, player_id: int, game_id: int, value: int) -> Score:
        """
        Отправить результат игры.
        
        Правила:
        - Игрок должен существовать
        - Игра должна существовать
        - Очки не могут быть отрицательными
        
        Args:
            player_id: Идентификатор игрока
            game_id: Идентификатор игры
            value: Количество очков
            
        Returns:
            Созданный результат
            
        Raises:
            ValueError: Если игрок или игра не найдены, или очки невалидны
        """
        # Проверка существования игрока
        player = self.player_repo.find_by_id(player_id)
        if not player:
            raise ValueError("Игрок не найден")
        
        # Проверка существования игры
        game = self.game_repo.find_by_id(game_id)
        if not game:
            raise ValueError("Игра не найдена")
        
        # Проверка валидности очков
        if value < 0:
            raise ValueError("Очки не могут быть отрицательными")
        
        # Создание результата
        score = Score(
            id=None,
            player_id=player_id,
            game_id=game_id,
            value=value,
            achieved_at=datetime.now()
        )
        
        return self.score_repo.insert(score)
    
    def get_player_scores(self, player_id: int) -> list[Score]:
        """
        Получить все результаты игрока.
        
        Args:
            player_id: Идентификатор игрока
            
        Returns:
            Список результатов игрока
        """
        return self.score_repo.find_by_player(player_id)