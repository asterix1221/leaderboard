from dataclasses import dataclass
from datetime import datetime


@dataclass
class Player:
    id: int | None
    username: str
    created_at: datetime

    def is_valid_username(self) -> bool:
        return bool(self.username) and len(self.username) <= 50
