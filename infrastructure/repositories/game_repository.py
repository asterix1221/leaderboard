"""
Репозиторий игр - CRUD операции для работы с играми в БД.
Реализует доступ к данным игр через SQLAlchemy.
"""

from typing import Protocol
from sqlalchemy.orm import Session
from entities.game import Game
from infrastructure.models.game_model import GameModel


class GameRepositoryProtocol(Protocol):
    """
    Интерфейс репозитория игр.
    Определяет контракт для операций с играми.
    """
    
    def insert(self, game: Game) -> Game:
        """Создать новую игру."""
        ...
    
    def find_by_id(self, game_id: int) -> Game | None:
        """Найти игру по ID."""
        ...
    
    def find_by_name(self, name: str) -> Game | None:
        """Найти игру по названию."""
        ...
    
    def get_all(self) -> list[Game]:
        """Получить все игры."""
        ...


class GameRepository:
    """
    Реализация репозитория игр для SQLite.
    """
    
    def __init__(self, db: Session):
        """
        Инициализация репозитория.
        
        Args:
            db: Сессия SQLAlchemy
        """
        self.db = db
    
    def insert(self, game: Game) -> Game:
        """
        Создать новую игру в базе данных.
        
        Args:
            game: Доменная сущность игры
            
        Returns:
            Созданная игра с присвоенным ID
        """
        db_game = GameModel(
            name=game.name,
            description=game.description
        )
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        
        # Обновляем ID в доменной сущности
        game.id = db_game.id
        return game
    
    def find_by_id(self, game_id: int) -> Game | None:
        """
        Найти игру по идентификатору.
        
        Args:
            game_id: Идентификатор игры
            
        Returns:
            Доменная сущность игры или None
        """
        db_game = self.db.query(GameModel).filter(GameModel.id == game_id).first()
        if db_game is None:
            return None
        
        return Game(
            id=db_game.id,
            name=db_game.name,
            description=db_game.description
        )
    
    def find_by_name(self, name: str) -> Game | None:
        """
        Найти игру по названию.
        
        Args:
            name: Название игры
            
        Returns:
            Доменная сущность игры или None
        """
        db_game = self.db.query(GameModel).filter(GameModel.name == name).first()
        if db_game is None:
            return None
        
        return Game(
            id=db_game.id,
            name=db_game.name,
            description=db_game.description
        )
    
    def get_all(self) -> list[Game]:
        """
        Получить все игры из базы данных.
        
        Returns:
            Список доменных сущностей игр
        """
        db_games = self.db.query(GameModel).all()
        return [
            Game(
                id=g.id,
                name=g.name,
                description=g.description
            )
            for g in db_games
        ]