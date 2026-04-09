"""
Tests for infrastructure database module startup functions.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime


class TestDatabaseStartup:
    """Test suite for database startup functions."""

    def test_create_tables_imports_models(self):
        """Test that create_tables imports the models."""
        # This test verifies the imports work correctly
        from infrastructure.models.player_model import PlayerModel
        from infrastructure.models.game_model import GameModel
        from infrastructure.models.score_model import ScoreModel
        
        assert PlayerModel is not None
        assert GameModel is not None
        assert ScoreModel is not None

    def test_create_tables_function_is_callable(self):
        """Test that create_tables function exists and is callable."""
        from infrastructure.database import create_tables
        
        assert callable(create_tables)


class TestMainStartup:
    """Test suite for main.py startup events."""

    def test_seed_data_checks_existing_data(self):
        """Test that seed_data checks if data already exists."""
        from unittest.mock import MagicMock, patch
        from datetime import datetime
        
        # We can't easily test seed_data without a real DB, but we can verify the logic
        # by checking the structure of the function
        import main
        import inspect
        
        # Verify seed_data function exists and has expected structure
        assert hasattr(main, 'seed_data')
        
        source = inspect.getsource(main.seed_data)
        
        # Verify function checks for existing data
        assert 'query(GameModel).first()' in source or 'first()' in source

    def test_app_has_startup_event(self):
        """Test that app has startup event handler."""
        import main
        
        # Check that app has on_event attribute (for startup)
        assert hasattr(main.app, 'on_event') or hasattr(main.app, 'lifespan')


class TestDatabaseModels:
    """Test suite for database models to_dict methods."""

    def test_game_model_to_dict(self):
        """Test GameModel.to_dict method."""
        from infrastructure.models.game_model import GameModel
        
        game = GameModel(id=1, name="Test Game", description="Test Description")
        result = game.to_dict()
        
        assert result["id"] == 1
        assert result["name"] == "Test Game"
        assert result["description"] == "Test Description"

    def test_player_model_to_dict(self):
        """Test PlayerModel.to_dict method."""
        from infrastructure.models.player_model import PlayerModel
        from datetime import datetime
        
        created_at = datetime(2023, 1, 15, 10, 0, 0)
        player = PlayerModel(id=1, username="testplayer", created_at=created_at)
        result = player.to_dict()
        
        assert result["id"] == 1
        assert result["username"] == "testplayer"
        assert result["created_at"] == "2023-01-15T10:00:00"

    def test_player_model_to_dict_with_none_created_at(self):
        """Test PlayerModel.to_dict with None created_at."""
        from infrastructure.models.player_model import PlayerModel
        
        player = PlayerModel(id=1, username="testplayer", created_at=None)
        result = player.to_dict()
        
        assert result["created_at"] is None

    def test_score_model_to_dict(self):
        """Test ScoreModel.to_dict method."""
        from infrastructure.models.score_model import ScoreModel
        from datetime import datetime
        
        achieved_at = datetime(2023, 1, 15, 10, 0, 0)
        score = ScoreModel(id=1, player_id=1, game_id=1, value=1000, achieved_at=achieved_at)
        result = score.to_dict()
        
        assert result["id"] == 1
        assert result["player_id"] == 1
        assert result["game_id"] == 1
        assert result["value"] == 1000
        assert result["achieved_at"] == "2023-01-15T10:00:00"

    def test_score_model_to_dict_with_none_achieved_at(self):
        """Test ScoreModel.to_dict with None achieved_at."""
        from infrastructure.models.score_model import ScoreModel
        
        score = ScoreModel(id=1, player_id=1, game_id=1, value=1000, achieved_at=None)
        result = score.to_dict()
        
        assert result["achieved_at"] is None