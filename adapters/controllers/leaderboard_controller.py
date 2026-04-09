from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from infrastructure import get_db, PlayerRepository, GameRepository, ScoreRepository
from use_cases import LeaderboardUseCases
from adapters.schemas import LeaderboardResponse, LeaderboardEntrySchema

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

@router.get("/{game_id}", response_model=LeaderboardResponse)
def get_leaderboard(
    game_id: int,
    limit: int = Query(default=10, ge=1, le=100, description="Количество записей"),
    db: Session = Depends(get_db)
):
    player_repo = PlayerRepository(db)
    game_repo = GameRepository(db)
    score_repo = ScoreRepository(db)

    use_case = LeaderboardUseCases(score_repo, game_repo)

    try:
        entries = use_case.get_leaderboard(game_id, limit)

        return LeaderboardResponse(
            game_id=game_id,
            entries=[
                LeaderboardEntrySchema(
                    rank=e.rank,
                    player_id=e.player_id,
                    username=e.username,
                    value=e.value,
                    achieved_at=e.achieved_at
                )
                for e in entries
            ]
        )
    except ValueError as e:
        msg = str(e)
        if "не найден" in msg or "не найдена" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)
