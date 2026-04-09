"""
Tests for the LeaderboardUseCases.
Verifies business logic for leaderboard operations.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from entities.game import Game
from use_cases.leaderboard_use_cases import LeaderboardEntry


class TestLeaderboardUseCases:
    """Test suite for LeaderboardUseCases."""

    def test_get_leaderboard_success(self, leaderboard_use_cases):
        """Test getting leaderboard for existing game."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        raw_scores = [
            {"player_id": 1, "username": "player1", "value": 1000, "achieved_at": datetime.now()},
            {"player_id": 2, "username": "player2", "value": 800, "achieved_at": datetime.now()},
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert len(result) == 2
        assert result[0].rank == 1
        assert result[0].username == "player1"
        assert result[0].value == 1000

    def test_get_leaderboard_raises_error_for_nonexistent_game(self, leaderboard_use_cases):
        """Test that getting leaderboard for non-existent game raises ValueError."""
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=None)
        
        with pytest.raises(ValueError) as exc_info:
            leaderboard_use_cases.get_leaderboard(999, 10)
        
        assert "Игра не найдена" in str(exc_info.value)

    def test_get_leaderboard_returns_empty_list_when_no_scores(self, leaderboard_use_cases):
        """Test that getting leaderboard returns empty list when no scores."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=[])
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert result == []

    def test_get_leaderboard_respects_limit(self, leaderboard_use_cases):
        """Test that get_leaderboard respects the limit parameter."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        # Return exactly 5 items to match the limit
        raw_scores = [
            {"player_id": i, "username": f"player{i}", "value": 1000 - i * 100, "achieved_at": datetime.now()}
            for i in range(1, 6)
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 5)
        
        assert len(result) == 5

    def test_get_leaderboard_assigns_ranks(self, leaderboard_use_cases):
        """Test that get_leaderboard assigns correct ranks."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        raw_scores = [
            {"player_id": 1, "username": "player1", "value": 1000, "achieved_at": datetime.now()},
            {"player_id": 2, "username": "player2", "value": 800, "achieved_at": datetime.now()},
            {"player_id": 3, "username": "player3", "value": 600, "achieved_at": datetime.now()},
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert result[0].rank == 1
        assert result[1].rank == 2
        assert result[2].rank == 3

    def test_get_leaderboard_includes_player_id(self, leaderboard_use_cases):
        """Test that leaderboard entries include player_id."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        raw_scores = [
            {"player_id": 42, "username": "topplayer", "value": 5000, "achieved_at": datetime.now()},
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert result[0].player_id == 42

    def test_get_leaderboard_default_limit(self, leaderboard_use_cases):
        """Test that get_leaderboard uses default limit of 10."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=[])
        
        result = leaderboard_use_cases.get_leaderboard(1)
        
        leaderboard_use_cases.score_repo.get_top_scores.assert_called_with(1, 10)

    def test_get_leaderboard_includes_achieved_at_as_isoformat(self, leaderboard_use_cases):
        """Test that achieved_at is converted to isoformat string."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        achieved_at = datetime(2023, 1, 15, 10, 30, 0)
        raw_scores = [
            {"player_id": 1, "username": "player1", "value": 1000, "achieved_at": achieved_at},
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert result[0].achieved_at == "2023-01-15T10:30:00"

    def test_get_leaderboard_handles_none_achieved_at(self, leaderboard_use_cases):
        """Test that leaderboard handles None achieved_at."""
        game = Game(id=1, name="Test Game", description="Test")
        leaderboard_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        raw_scores = [
            {"player_id": 1, "username": "player1", "value": 1000, "achieved_at": None},
        ]
        leaderboard_use_cases.score_repo.get_top_scores = Mock(return_value=raw_scores)
        
        result = leaderboard_use_cases.get_leaderboard(1, 10)
        
        assert result[0].achieved_at == ""