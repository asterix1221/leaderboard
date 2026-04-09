"""
Контроллер результатов - REST API для работы с результатами.
Содержит эндпоинты для отправки и получения результатов игр.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure import get_db, PlayerRepository, GameRepository, ScoreRepository
from use_cases import ScoreUseCases
from adapters.schemas import ScoreCreate, ScoreResponse

# Создание роутера
router = APIRouter(prefix="/api/scores", tags=["scores"])


@router.post("", response_model=ScoreResponse, status_code=201)
def submit_score(score_data: ScoreCreate, db: Session = Depends(get_db)):
    """
    Отправить результат игры.
    
    Параметры:
        score_data: Данные результата
        db: Сессия БД
        
    Returns:
        Созданный результат
    """
    player_repo = PlayerRepository(db)
    game_repo = GameRepository(db)
    score_repo = ScoreRepository(db)
    
    use_case = ScoreUseCases(score_repo, player_repo, game_repo)
    
    try:
        score = use_case.submit_score(
            player_id=score_data.player_id,
            game_id=score_data.game_id,
            value=score_data.value
        )
        return ScoreResponse(
            id=score.id,
            player_id=score.player_id,
            game_id=score.game_id,
            value=score.value,
            achieved_at=score.achieved_at
        )
    except ValueError as e:
        msg = str(e)
        if "не найден" in msg or "не найдена" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@router.get("/player/{player_id}", response_model=list[ScoreResponse])
def get_player_scores(player_id: int, db: Session = Depends(get_db)):
    """
    Получить все результаты игрока.
    
    Параметры:
        player_id: Идентификатор игрока
        db: Сессия БД
        
    Returns:
        Список результатов игрока
    """
    player_repo = PlayerRepository(db)
    game_repo = GameRepository(db)
    score_repo = ScoreRepository(db)
    
    use_case = ScoreUseCases(score_repo, player_repo, game_repo)
    
    scores = use_case.get_player_scores(player_id)
    
    return [
        ScoreResponse(
            id=s.id,
            player_id=s.player_id,
            game_id=s.game_id,
            value=s.value,
            achieved_at=s.achieved_at
        )
        for s in scores
    ]