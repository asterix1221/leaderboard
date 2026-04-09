from dataclasses import dataclass
from infrastructure.repositories import ScoreRepositoryProtocol, GameRepositoryProtocol

@dataclass
class LeaderboardEntry:
    rank: int
    player_id: int
    username: str
    value: int
    achieved_at: str

class LeaderboardUseCases:
    def __init__(
        self,
        score_repo: ScoreRepositoryProtocol,
        game_repo: GameRepositoryProtocol
    ):
        self.score_repo = score_repo
        self.game_repo = game_repo

    def get_leaderboard(self, game_id: int, limit: int = 10) -> list[LeaderboardEntry]:
        game = self.game_repo.find_by_id(game_id)
        if not game:
            raise ValueError("Игра не найдена")

        raw_scores = self.score_repo.get_top_scores(game_id, limit)

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
