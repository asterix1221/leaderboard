"""
Репозиторий игроков - CRUD операции для работы с игроками в БД.
Реализует доступ к данным игроков через SQLAlchemy.
"""

from typing import Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from entities.player import Player
from infrastructure.models.player_model import PlayerModel


class PlayerRepositoryProtocol(Protocol):
    """
    Интерфейс репозитория игроков.
    Определяет контракт для операций с игроками.
    """
    
    def insert(self, player: Player) -> Player:
        """Создать нового игрока."""
        ...
    
    def find_by_id(self, player_id: int) -> Player | None:
        """Найти игрока по ID."""
        ...
    
    def find_by_username(self, username: str) -> Player | None:
        """Найти игрока по имени пользователя."""
        ...
    
    def get_all(self) -> list[Player]:
        """Получить всех игроков."""
        ...


class PlayerRepository:
    """
    Реализация репозитория игроков для SQLite.
    """
    
    def __init__(self, db: Session):
        """
        Инициализация репозитория.
        
        Args:
            db: Сессия SQLAlchemy
        """
        self.db = db
    
    def insert(self, player: Player) -> Player:
        """
        Создать нового игрока в базе данных.
        
        Args:
            player: Доменная сущность игрока
            
        Returns:
            Созданный игрок с присвоенным ID
        """
        db_player = PlayerModel(
            username=player.username,
            created_at=player.created_at
        )
        self.db.add(db_player)
        self.db.commit()
        self.db.refresh(db_player)
        
        # Обновляем ID в доменной сущности
        player.id = db_player.id
        return player
    
    def find_by_id(self, player_id: int) -> Player | None:
        """
        Найти игрока по идентификатору.
        
        Args:
            player_id: Идентификатор игрока
            
        Returns:
            Доменная сущность игрока или None
        """
        db_player = self.db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
        if db_player is None:
            return None
        
        return Player(
            id=db_player.id,
            username=db_player.username,
            created_at=db_player.created_at
        )
    
    def find_by_username(self, username: str) -> Player | None:
        """
        Найти игрока по имени пользователя.
        
        Args:
            username: Имя пользователя
            
        Returns:
            Доменная сущность игрока или None
        """
        db_player = self.db.query(PlayerModel).filter(PlayerModel.username == username).first()
        if db_player is None:
            return None
        
        return Player(
            id=db_player.id,
            username=db_player.username,
            created_at=db_player.created_at
        )
    
    def get_all(self) -> list[Player]:
        """
        Получить всех игроков из базы данных.
        
        Returns:
            Список доменных сущностей игроков
        """
        db_players = self.db.query(PlayerModel).all()
        return [
            Player(
                id=p.id,
                username=p.username,
                created_at=p.created_at
            )
            for p in db_players
        ]