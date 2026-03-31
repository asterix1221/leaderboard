"""
Tests for the Score Controller (REST API).
Verifies HTTP endpoints for score operations.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime


class TestScoreController:
    """Test suite for score API endpoints."""

    def test_submit_score_success(self):
        """Test successful score submission."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                
                from entities.player import Player
                from entities.game import Game
                from entities.score import Score
                
                mock_player_repo.find_by_id.return_value = Player(
                    id=1, username="player1", created_at=datetime.now()
                )
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                mock_score_repo.insert.return_value = Score(
                    id=1, player_id=1, game_id=1, value=1000, achieved_at=datetime.now()
                )
                
                client = TestClient(app)
                response = client.post(
                    "/api/scores",
                    json={"player_id": 1, "game_id": 1, "value": 1000}
                )
                
                assert response.status_code == 201
                data = response.json()
                assert data["value"] == 1000

    def test_submit_score_invalid_player(self):
        """Test that submitting score for invalid player returns 404."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository'):
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                mock_player_repo.find_by_id.return_value = None
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                client = TestClient(app)
                response = client.post(
                    "/api/scores",
                    json={"player_id": 999, "game_id": 1, "value": 1000}
                )
                
                assert response.status_code == 404

    def test_submit_score_invalid_game(self):
        """Test that submitting score for invalid game returns 404."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository'):
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                from entities.player import Player
                mock_player_repo.find_by_id.return_value = Player(
                    id=1, username="player1", created_at=datetime.now()
                )
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                mock_game_repo.find_by_id.return_value = None
                
                client = TestClient(app)
                response = client.post(
                    "/api/scores",
                    json={"player_id": 1, "game_id": 999, "value": 1000}
                )
                
                assert response.status_code == 404

    def test_submit_score_negative_value(self):
        """Test that submitting negative score returns 400.
        
        Note: Since the Pydantic schema already validates non-negative values (ge=0),
        negative values are rejected at the validation layer (422) rather than
        the use case layer (400). This test documents that behavior.
        """
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository'):
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                from entities.player import Player
                from entities.game import Game
                
                mock_player_repo.find_by_id.return_value = Player(
                    id=1, username="player1", created_at=datetime.now()
                )
                mock_game_repo.find_by_id.return_value = Game(
                    id=1, name="Game 1", description="Desc"
                )
                
                client = TestClient(app)
                response = client.post(
                    "/api/scores",
                    json={"player_id": 1, "game_id": 1, "value": -100}
                )
                
                # Pydantic validation rejects negative value before it reaches the use case
                assert response.status_code == 422

    def test_submit_score_negative_value_pydantic(self):
        """Test that Pydantic rejects negative score value."""
        from main import app
        
        client = TestClient(app)
        response = client.post(
            "/api/scores",
            json={"player_id": 1, "game_id": 1, "value": -1}
        )
        
        # Pydantic validation should reject negative value
        assert response.status_code == 422

    def test_get_player_scores(self):
        """Test getting all scores for a player."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                
                from entities.score import Score
                
                mock_score_repo.find_by_player.return_value = [
                    Score(id=1, player_id=1, game_id=1, value=1000, achieved_at=datetime.now()),
                    Score(id=2, player_id=1, game_id=1, value=2000, achieved_at=datetime.now()),
                ]
                
                client = TestClient(app)
                response = client.get("/api/scores/player/1")
                
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2

    def test_get_player_scores_empty(self):
        """Test getting scores for player with no scores."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.score_controller.PlayerRepository') as mock_player_repo_class, \
                 patch('adapters.controllers.score_controller.GameRepository') as mock_game_repo_class, \
                 patch('adapters.controllers.score_controller.ScoreRepository') as mock_score_repo_class:
                
                mock_player_repo = Mock()
                mock_player_repo_class.return_value = mock_player_repo
                
                mock_game_repo = Mock()
                mock_game_repo_class.return_value = mock_game_repo
                
                mock_score_repo = Mock()
                mock_score_repo_class.return_value = mock_score_repo
                mock_score_repo.find_by_player.return_value = []
                
                client = TestClient(app)
                response = client.get("/api/scores/player/1")
                
                assert response.status_code == 200
                assert response.json() == []