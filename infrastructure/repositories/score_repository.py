"""
Репозиторий результатов - CRUD операции для работы с результатами в БД.
Реализует доступ к данным результатов через SQLAlchemy.
"""

from typing import Protocol
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from entities.score import Score
from infrastructure.models.score_model import ScoreModel
from infrastructure.models.player_model import PlayerModel


class ScoreRepositoryProtocol(Protocol):
    """
    Интерфейс репозитория результатов.
    Определяет контракт для операций с результатами.
    """
    
    def insert(self, score: Score) -> Score:
        """Создать новый результат."""
        ...
    
    def find_by_id(self, score_id: int) -> Score | None:
        """Найти результат по ID."""
        ...
    
    def find_by_player(self, player_id: int) -> list[Score]:
        """Найти все результаты игрока."""
        ...
    
    def get_top_scores(self, game_id: int, limit: int) -> list[dict]:
        """Получить топ результатов для игры (лучший результат каждого игрока)."""
        ...


class ScoreRepository:
    """
    Реализация репозитория результатов для SQLite.
    """
    
    def __init__(self, db: Session):
        """
        Инициализация репозитория.
        
        Args:
            db: Сессия SQLAlchemy
        """
        self.db = db
    
    def insert(self, score: Score) -> Score:
        """
        Создать новый результат в базе данных.
        
        Args:
            score: Доменная сущность результата
            
        Returns:
            Созданный результат с присвоенным ID
        """
        db_score = ScoreModel(
            player_id=score.player_id,
            game_id=score.game_id,
            value=score.value,
            achieved_at=score.achieved_at
        )
        self.db.add(db_score)
        self.db.commit()
        self.db.refresh(db_score)
        
        # Обновляем ID в доменной сущности
        score.id = db_score.id
        return score
    
    def find_by_id(self, score_id: int) -> Score | None:
        """
        Найти результат по идентификатору.
        
        Args:
            score_id: Идентификатор результата
            
        Returns:
            Доменная сущность результата или None
        """
        db_score = self.db.query(ScoreModel).filter(ScoreModel.id == score_id).first()
        if db_score is None:
            return None
        
        return Score(
            id=db_score.id,
            player_id=db_score.player_id,
            game_id=db_score.game_id,
            value=db_score.value,
            achieved_at=db_score.achieved_at
        )
    
    def find_by_player(self, player_id: int) -> list[Score]:
        """
        Найти все результаты конкретного игрока.
        
        Args:
            player_id: Идентификатор игрока
            
        Returns:
            Список доменных сущностей результатов
        """
        db_scores = self.db.query(ScoreModel).filter(ScoreModel.player_id == player_id).all()
        return [
            Score(
                id=s.id,
                player_id=s.player_id,
                game_id=s.game_id,
                value=s.value,
                achieved_at=s.achieved_at
            )
            for s in db_scores
        ]
    
    def get_top_scores(self, game_id: int, limit: int) -> list[dict]:
        """
        Получить лучшие результаты для игры.
        Для каждого игрока берётся запись с максимальными очками.
        Возвращается дата именно той записи, где был установлен рекорд.
        
        Args:
            game_id: Идентификатор игры
            limit: Количество записей в лидерборде
            
        Returns:
            Список словарей с данными игроков и их лучшими очками
        """
        # Подзапрос: для каждого игрока находим его лучший результат
        subquery = (
            self.db.query(
                ScoreModel.player_id,
                func.max(ScoreModel.value).label('best_score')
            )
            .filter(ScoreModel.game_id == game_id)
            .group_by(ScoreModel.player_id)
            .subquery()
        )
        
        # Джоиним с оригинальной таблицей чтобы получить дату записи с рекордом
        results = (
            self.db.query(
                ScoreModel.player_id,
                ScoreModel.value,
                ScoreModel.achieved_at,
                PlayerModel.username
            )
            .join(subquery, (ScoreModel.player_id == subquery.c.player_id) &
                            (ScoreModel.value == subquery.c.best_score))
            .join(PlayerModel, PlayerModel.id == ScoreModel.player_id)
            .filter(ScoreModel.game_id == game_id)
            .order_by(ScoreModel.value.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "player_id": r.player_id,
                "username": r.username,
                "value": r.value,
                "achieved_at": r.achieved_at
            }
            for r in results
        ]