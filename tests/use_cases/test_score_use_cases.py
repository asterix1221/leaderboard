"""
Tests for the ScoreUseCases.
Verifies business logic for score operations.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from entities.score import Score
from entities.player import Player
from entities.game import Game


class TestScoreUseCases:
    """Test suite for ScoreUseCases."""

    def test_submit_score_success(self, score_use_cases):
        """Test submitting a score with valid data."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        game = Game(id=1, name="Test Game", description="Test")
        
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=game)
        score_use_cases.score_repo.insert = Mock(
            return_value=Score(id=1, player_id=1, game_id=1, value=1000, achieved_at=datetime.now())
        )
        
        result = score_use_cases.submit_score(1, 1, 1000)
        
        assert result.value == 1000
        score_use_cases.score_repo.insert.assert_called_once()

    def test_submit_score_raises_error_for_invalid_player(self, score_use_cases):
        """Test that submitting score for non-existent player raises ValueError."""
        score_use_cases.player_repo.find_by_id = Mock(return_value=None)
        
        with pytest.raises(ValueError) as exc_info:
            score_use_cases.submit_score(999, 1, 1000)
        
        assert "Игрок не найден" in str(exc_info.value)

    def test_submit_score_raises_error_for_invalid_game(self, score_use_cases):
        """Test that submitting score for non-existent game raises ValueError."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=None)
        
        with pytest.raises(ValueError) as exc_info:
            score_use_cases.submit_score(1, 999, 1000)
        
        assert "Игра не найдена" in str(exc_info.value)

    def test_submit_score_raises_error_for_negative_value(self, score_use_cases):
        """Test that submitting negative score raises ValueError."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        game = Game(id=1, name="Test Game", description="Test")
        
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        with pytest.raises(ValueError) as exc_info:
            score_use_cases.submit_score(1, 1, -100)
        
        assert "не могут быть отрицательными" in str(exc_info.value)

    def test_submit_score_allows_zero_value(self, score_use_cases):
        """Test that submitting zero score is allowed."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        game = Game(id=1, name="Test Game", description="Test")
        
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=game)
        score_use_cases.score_repo.insert = Mock(
            return_value=Score(id=1, player_id=1, game_id=1, value=0, achieved_at=datetime.now())
        )
        
        result = score_use_cases.submit_score(1, 1, 0)
        
        assert result.value == 0

    def test_submit_score_allows_large_value(self, score_use_cases):
        """Test that submitting very large score is allowed."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        game = Game(id=1, name="Test Game", description="Test")
        
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=game)
        score_use_cases.score_repo.insert = Mock(
            return_value=Score(id=1, player_id=1, game_id=1, value=999999999, achieved_at=datetime.now())
        )
        
        result = score_use_cases.submit_score(1, 1, 999999999)
        
        assert result.value == 999999999

    def test_get_player_scores_returns_list(self, score_use_cases):
        """Test that get_player_scores returns list of scores."""
        scores = [
            Score(id=1, player_id=1, game_id=1, value=1000, achieved_at=datetime.now()),
            Score(id=2, player_id=1, game_id=1, value=2000, achieved_at=datetime.now()),
        ]
        score_use_cases.score_repo.find_by_player = Mock(return_value=scores)
        
        result = score_use_cases.get_player_scores(1)
        
        assert len(result) == 2

    def test_get_player_scores_returns_empty_list_when_no_scores(self, score_use_cases):
        """Test that get_player_scores returns empty list when no scores."""
        score_use_cases.score_repo.find_by_player = Mock(return_value=[])
        
        result = score_use_cases.get_player_scores(1)
        
        assert result == []

    def test_submit_score_calls_insert_with_correct_data(self, score_use_cases):
        """Test that submit_score calls insert with correct entity."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        game = Game(id=1, name="Test Game", description="Test")
        
        score_use_cases.player_repo.find_by_id = Mock(return_value=player)
        score_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        inserted_score = Score(id=1, player_id=1, game_id=1, value=5000, achieved_at=datetime.now())
        score_use_cases.score_repo.insert = Mock(return_value=inserted_score)
        
        score_use_cases.submit_score(1, 1, 5000)
        
        call_args = score_use_cases.score_repo.insert.call_args[0][0]
        assert call_args.player_id == 1
        assert call_args.game_id == 1
        assert call_args.value == 5000