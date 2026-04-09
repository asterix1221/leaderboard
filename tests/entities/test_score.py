"""
Tests for the Score entity.
Verifies business logic and validation rules.
"""

import pytest
from datetime import datetime
from entities.score import Score


class TestScoreEntity:
    """Test suite for Score entity."""

    def test_score_creation_with_valid_data(self):
        """Test creating a score with valid data."""
        achieved_at = datetime.now()
        score = Score(
            id=1,
            player_id=10,
            game_id=5,
            value=1000,
            achieved_at=achieved_at
        )
        
        assert score.id == 1
        assert score.player_id == 10
        assert score.game_id == 5
        assert score.value == 1000
        assert score.achieved_at == achieved_at

    def test_score_creation_with_null_id(self):
        """Test creating a score before saving to database."""
        achieved_at = datetime.now()
        score = Score(
            id=None,
            player_id=10,
            game_id=5,
            value=500,
            achieved_at=achieved_at
        )
        
        assert score.id is None
        assert score.value == 500

    def test_is_valid_returns_true_for_zero_value(self):
        """Test is_valid returns True when value is zero."""
        score = Score(
            id=None,
            player_id=1,
            game_id=1,
            value=0,
            achieved_at=datetime.now()
        )
        
        assert score.is_valid() is True

    def test_is_valid_returns_true_for_positive_value(self):
        """Test is_valid returns True for positive value."""
        score = Score(
            id=None,
            player_id=1,
            game_id=1,
            value=5000,
            achieved_at=datetime.now()
        )
        
        assert score.is_valid() is True

    def test_is_valid_returns_false_for_negative_value(self):
        """Test is_valid returns False for negative value."""
        score = Score(
            id=None,
            player_id=1,
            game_id=1,
            value=-100,
            achieved_at=datetime.now()
        )
        
        assert score.is_valid() is False

    def test_is_valid_returns_true_for_large_value(self):
        """Test is_valid returns True for very large value."""
        score = Score(
            id=None,
            player_id=1,
            game_id=1,
            value=999999999,
            achieved_at=datetime.now()
        )
        
        assert score.is_valid() is True

    def test_score_with_different_player_and_game_ids(self):
        """Test score with various player and game IDs."""
        score = Score(
            id=1,
            player_id=100,
            game_id=200,
            value=12345,
            achieved_at=datetime.now()
        )
        
        assert score.player_id == 100
        assert score.game_id == 200
        assert score.is_valid() is True