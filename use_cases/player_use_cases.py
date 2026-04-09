"""
Сценарии использования для работы с игроками.
Содержит бизнес-логику регистрации и получения информации об игроках.
"""

from datetime import datetime
from entities.player import Player
from infrastructure.repositories import PlayerRepositoryProtocol


class PlayerUseCases:
    """
    Сценарии использования для работы с игроками.
    Реализует бизнес-логику, связанную с игроками.
    """
    
    def __init__(self, player_repo: PlayerRepositoryProtocol):
        """
        Инициализация сценариев использования.
        
        Args:
            player_repo: Репозиторий игроков (внедрение зависимости)
        """
        self.player_repo = player_repo
    
    def register_player(self, username: str) -> Player:
        """
        Зарегистрировать нового игрока.
        
        Правила:
        - Имя пользователя должно быть уникальным
        - Имя не может быть пустым
        - Имя не может быть длиннее 50 символов
        
        Args:
            username: Имя пользователя
            
        Returns:
            Созданный игрок
            
        Raises:
            ValueError: Если имя пользователя уже занято или невалидно
        """
        # Проверка валидности имени
        if not username or len(username) > 50:
            raise ValueError("Имя пользователя должно быть от 1 до 50 символов")
        
        # Проверка уникальности имени
        existing = self.player_repo.find_by_username(username)
        if existing:
            raise ValueError("Имя пользователя уже занято")
        
        # Создание игрока
        player = Player(
            id=None,
            username=username,
            created_at=datetime.now()
        )
        
        return self.player_repo.insert(player)
    
    def get_player(self, player_id: int) -> Player | None:
        """
        Получить информацию об игроке по ID.
        
        Args:
            player_id: Идентификатор игрока
            
        Returns:
            Игрок или None если не найден
        """
        return self.player_repo.find_by_id(player_id)
    
    def get_player_by_username(self, username: str) -> Player | None:
        """
        Получить информацию об игроке по имени пользователя.
        
        Args:
            username: Имя пользователя
            
        Returns:
            Игрок или None если не найден
        """
        return self.player_repo.find_by_username(username)
    
    def get_all_players(self) -> list[Player]:
        """
        Получить всех зарегистрированных игроков.
        
        Returns:
            Список всех игроков
        """
        return self.player_repo.get_all()