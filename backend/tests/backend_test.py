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
        assert response.json['message'] == ('Gra zakończona: X')

        # 3. Check if X won
        response = self.client.get(f'/api/reset?gameId={game_id}')
        assert response.status_code == 200
        # Check the message or status for the win
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

    def test_invalid_move(self):
        # Start a new game
        response = self.client.get('/api/start')
        game_id = response.json['gameId']

        # Make an invalid move (e.g., outside the board)
        response = self.client.post('/api/move', json={'row': 3, 'col': 3, 'gameId': game_id})
        assert response.status_code == 400

        # Make a move and then another move on the same spot
        self.client.post('/api/move', json={'row': 0, 'col': 0, 'gameId': game_id})
        response = self.client.post('/api/move', json={'row': 0, 'col': 0, 'gameId': game_id})
        assert response.status_code == 400

    def test_game_draw(self):


        # Start a new game and play moves leading to a draw
        response = self.client.get('/api/start')
        game_id = response.json['gameId']
        moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (1, 2), (2, 1), (2, 2)]
        for row, col in moves:
            response = self.client.post('/api/move', json={'row': row, 'col': col, 'gameId': game_id})
            assert response.status_code == 200 or (row, col) == moves[-1]
        assert response.json['message'] == ('Gra zakończona: X')



    def test_restart_game(self):
        # Start a new game
        response = self.client.get('/api/start')
        game_id = response.json['gameId']

        # Make some moves
        self.client.post('/api/move', json={'row': 0, 'col': 0, 'gameId': game_id})
        self.client.post('/api/move', json={'row': 1, 'col': 1, 'gameId': game_id})

        # Reset the game
        self.client.get(f'/api/reset?gameId={game_id}')

        # Check if the board is reset
        response = self.client.get(f'/api/start?gameId={game_id}')
        assert all(cell == '' for row in response.json['boardState'] for cell in row)

    def test_game_over_condition(self):
        # Start a new game and play a winning combination
        response = self.client.get('/api/start')
        game_id = response.json['gameId']
        winning_moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]

        for row, col in winning_moves:
            self.client.post('/api/move', json={'row': row, 'col': col, 'gameId': game_id})


        # Attempt to make a move after the game is over
        response = self.client.post('/api/move', json={'row': 2, 'col': 2, 'gameId': game_id})
        assert response.status_code == 400
        assert response.json['error'] == ('Nie można grać w zakończoną grę.')
