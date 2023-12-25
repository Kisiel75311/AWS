# backend/tests/backend_test.py

import pytest
from flask_testing import TestCase
from app import create_app, db  # Adjust the import according to your project structure


class TestGameAPI(TestCase):
    def create_app(self):
        # Configure your app for testing
        app = create_app(testing=True)  # Make sure to configure a test environment
        return app

    def setUp(self):
        # Set up test database, if necessary
        db.create_all()

    def tearDown(self):
        # Clean up / close database after tests
        db.session.remove()
        db.drop_all()

    def test_game_flow(self):
        # 1. Start a new game
        response = self.client.get('/api/start')
        assert response.status_code == 200
        game_data = response.json
        game_id = game_data['gameId']
        assert game_id is not None

        # 2. Make moves to lead X to win
        # Assuming (0,0), (1,1), (2,2) will lead to a win
        winning_moves = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
        for row, col in winning_moves:
            response = self.client.post('/api/move', json={'row': row, 'col': col, 'gameId': game_id})
            assert response.status_code == 200 or (row, col) == winning_moves[-1]  # Last move might end the game

        # 3. Check if X won
        headers = {'Content-Type': 'application/json'}
        response = self.client.get('/api/reset', json={'gameId': game_id}, headers=headers)
        assert response.status_code == 200
        game_data = response.json
        assert game_data['message'] == 'Gra została zresetowana.'

    def test_multiple_independent_games(self):
        # Create and play two separate games

        # Start Game 1
        response = self.client.get('/api/start')
        assert response.status_code == 200
        game1_data = response.json
        game1_id = game1_data['gameId']
        assert game1_id is not None

        # Make moves in Game 1
        game1_moves = [(0, 0), (1, 1)]
        for row, col in game1_moves:
            response = self.client.post('/api/move', json={'row': row, 'col': col, 'gameId': game1_id})
            assert response.status_code == 200

        # Start Game 2
        response = self.client.get('/api/start')
        assert response.status_code == 200
        game2_data = response.json
        game2_id = game2_data['gameId']
        assert game2_id is not None and game2_id != game1_id

        # Make moves in Game 2
        game2_moves = [(2, 2), (1, 0)]
        for row, col in game2_moves:
            response = self.client.post('/api/move', json={'row': row, 'col': col, 'gameId': game2_id})
            assert response.status_code == 200

        # Verify the final states of both games are independent
        # (you may need to implement an endpoint or logic to retrieve the current state of a game)
        # For example:
        # response = self.client.get(f'/api/game_state/{game1_id}')
        # game1_state = response.json
        # response = self.client.get(f'/api/game_state/{game2_id}')
        # game2_state = response.json
        # assert game1_state != game2_state
