"""
Tests for the Leaderboard Controller (REST API).
Verifies HTTP endpoints for leaderboard operations.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime


class TestLeaderboardController:
    """Test suite for leaderboard API endpoints."""

    def test_get_leaderboard_success(self):
        """Test getting leaderboard for a game."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.leaderboard_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                
                from entities.game import Game
                
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                
                mock_score_repo.get_top_scores.return_value = [
                    {"player_id": 1, "username": "player1", "value": 1000, "achieved_at": datetime.now()},
                    {"player_id": 2, "username": "player2", "value": 800, "achieved_at": datetime.now()},
                ]
                
                client = TestClient(app)
                response = client.get("/api/leaderboard/1")
                
                assert response.status_code == 200
                data = response.json()
                assert data["game_id"] == 1
                assert len(data["entries"]) == 2
                assert data["entries"][0]["rank"] == 1
                assert data["entries"][0]["value"] == 1000

    def test_get_leaderboard_invalid_game(self):
        """Test that getting leaderboard for invalid game returns 404."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.leaderboard_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                mock_game_repo.find_by_id.return_value = None
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                
                client = TestClient(app)
                response = client.get("/api/leaderboard/999")
                
                assert response.status_code == 404

    def test_get_leaderboard_empty(self):
        """Test getting leaderboard when no scores exist."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.leaderboard_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                from entities.game import Game
                
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                mock_score_repo.get_top_scores.return_value = []
                
                client = TestClient(app)
                response = client.get("/api/leaderboard/1")
                
                assert response.status_code == 200
                data = response.json()
                assert data["entries"] == []

    def test_get_leaderboard_with_custom_limit(self):
        """Test getting leaderboard with custom limit."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.leaderboard_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                from entities.game import Game
                
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                mock_score_repo.get_top_scores.return_value = [
                    {"player_id": i, "username": f"player{i}", "value": 1000 - i * 100, "achieved_at": datetime.now()}
                    for i in range(1, 6)
                ]
                
                client = TestClient(app)
                response = client.get("/api/leaderboard/1?limit=3")
                
                assert response.status_code == 200
                # The limit is passed to get_top_scores
                mock_score_repo.get_top_scores.assert_called_with(1, 3)

    def test_get_leaderboard_default_limit(self):
        """Test that default limit is 10."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.leaderboard_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.leaderboard_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                from entities.game import Game
                
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                mock_score_repo.get_top_scores.return_value = []
                
                client = TestClient(app)
                response = client.get("/api/leaderboard/1")
                
                assert response.status_code == 200
                mock_score_repo.get_top_scores.assert_called_with(1, 10)

    def test_get_leaderboard_limit_validation(self):
        """Test that limit must be at least 1."""
        from main import app
        
        client = TestClient(app)
        response = client.get("/api/leaderboard/1?limit=0")
        
        # FastAPI validation should reject limit < 1
        assert response.status_code == 422

    def test_get_leaderboard_limit_max_validation(self):
        """Test that limit must be at most 100."""
        from main import app
        
        client = TestClient(app)
        response = client.get("/api/leaderboard/1?limit=101")
        
        # FastAPI validation should reject limit > 100
        assert response.status_code == 422