# backend/tests/test_game_api.py
import logging
import unittest
from flask_jwt_extended import create_access_token
from api.game_api import game_blueprint
from models.player_model import Player
from models.game_model import Game
from app import build_app, db
from services.game_service import GameService
from game.TicTacToe import TicTacToe
import allure


@allure.feature('Game API')
class TestGameApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = build_app(testing=True)
        cls.client = cls.app.test_client()
        cls.game_service = GameService()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_player(self, name, password):
        player = Player(name=name, password=password)
        db.session.add(player)
        db.session.commit()
        return player

    def create_game(self, player1_id, player2_id=None):
        # Create a new game with player1
        game_id, board_state, current_player = GameService.create_new_game(player1_id)

        # Fetch the newly created game
        new_game = db.session.get(Game, game_id)

        # If player2 is provided, assign them to the game
        if player2_id:
            new_game.player2_id = player2_id
            player2 = Player.query.get(player2_id)
            player2.current_game_id = game_id
            db.session.commit()

        return new_game

    @allure.story('Test Start Game')
    def test_start_game(self):
        # Assume there is a valid player to make the requests
        player = self.create_player('Test Player', '123456')
        logging.info(f"Player ID: {player.id}")
        jwt_token = create_access_token(player.id)
        response = self.client.get('/api/start', headers={'Authorization': 'Bearer ' + jwt_token})
        response_data = response.get_data(as_text=True)
        logging.info(f"Response: {response_data}")
        self.assertEqual(200, response.status_code, f"Response data: {response_data}")

    @allure.story('Test Invalid Move')
    def test_invalid_move(self):
        # Tworzenie gracza
        player1 = self.create_player('Test Player1', '123456')
        player2 = self.create_player('Test Player2', '123456')

        # Tworzenie nowej gry
        new_game = self.create_game(player1.id)

        # Ustawienie gracza jako uczestnika gry
        player1.current_game_id = new_game.id
        player2.current_game_id = new_game.id
        new_game.player2_id = player2.id
        db.session.commit()

        # Tworzenie tokena JWT dla gracza
        token1 = create_access_token(player1.id)

        # Wykonywanie nieprawidłowego ruchu
        move_response = self.client.post('/api/move',
                                         json={'row': 19, 'col': 1, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})
        assert move_response.status_code == 400
        move_data = move_response.json
        assert move_data['message'] == 'Invalid move.'

    @allure.story('Test Valid Move')
    def test_valid_move(self):
        # Tworzenie gracza
        player1 = self.create_player('Test Player1', '123456')
        player2 = self.create_player('Test Player2', '123456')

        # Tworzenie nowej gry
        new_game = self.create_game(player1.id)

        # Ustawienie gracza jako uczestnika gry
        player1.current_game_id = new_game.id
        player2.current_game_id = new_game.id
        new_game.player2_id = player2.id
        db.session.commit()

        # Tworzenie tokena JWT dla gracza
        token1 = create_access_token(player1.id)

        # Wykonywanie prawidłowego ruchu
        move_response = self.client.post('/api/move',
                                         json={'row': 0, 'col': 1, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})

        # Sprawdzenie, czy odpowiedź jest sukcesem, w przeciwnym razie wyświetl szczegółowe informacje
        assert move_response.status_code == 200, f"Failed to make a valid move. Response: {move_response.get_data(as_text=True)}"

        move_data = move_response.json
        assert move_data[
                   'message'] == 'Move played successfully.', f"Unexpected response message: {move_data['message']}"

    @allure.story('Test Game Flow - Player 1 Wins')
    def test_game_flow_player1_win(self):
        # Create players
        player1 = self.create_player('Test Player1', '123456')
        player2 = self.create_player('Test Player2', '123456')

        # Create a new game
        new_game = self.create_game(player1.id)

        # Set each player as a participant in the game
        player1.current_game_id = new_game.id
        player2.current_game_id = new_game.id
        new_game.player2_id = player2.id
        db.session.commit()

        # Create JWT tokens for players
        token1 = create_access_token(player1.id)
        token2 = create_access_token(player2.id)

        # Implement a game flow where Player 1 makes winning moves
        # Assuming your winning condition is three in a row
        # Also assuming that 'row' and 'col' range is from 0 to 2 (3x3 board)

        # Player 1 makes move
        move_response = self.client.post('/api/move',
                                         json={'row': 0, 'col': 0, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})
        assert move_response.status_code == 200

        # Player 2 makes move
        move_response = self.client.post('/api/move',
                                         json={'row': 1, 'col': 0, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token2}'})
        assert move_response.status_code == 200

        # Player 1 makes move
        move_response = self.client.post('/api/move',
                                         json={'row': 0, 'col': 1, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})
        assert move_response.status_code == 200

        # Player 2 makes move
        move_response = self.client.post('/api/move',
                                         json={'row': 1, 'col': 1, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token2}'})
        assert move_response.status_code == 200

        # Player 1 makes the final move
        move_response = self.client.post('/api/move',
                                         json={'row': 0, 'col': 2, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})
        assert move_response.status_code == 200

        # Extract the response data
        move_data = move_response.get_json()

        # Check if the move was successful and the game is over
        assert move_data['message'] == "Move played successfully, game ended.", "Unexpected response message."

        # Fetch the updated game state to check if Player 1 is declared as the winner
        updated_game = db.session.get(Game, new_game.id)
        assert updated_game.game_over is True, "Game should be over."
        assert updated_game.winner == GameService.PLAYER_X, "Player 1 should be the winner."

        # Optionally, you can check the board state as well
        assert move_data['boardState'] == GameService.get_board_as_2d_array(
            updated_game.board_state), "Board state mismatch."

        # Fetch the updated player states to check ELO rating change
        updated_player1 = db.session.get(Player, player1.id)
        updated_player2 = db.session.get(Player, player2.id)
        self.assertEqual(updated_player1.elo_rating, 1015)
        self.assertEqual(updated_player2.elo_rating, 985)

    @allure.story('Test Game Flow - Draw Game')
    def test_game_flow_draw(self):
        # Create players
        player1 = self.create_player('Test Player1', '123456')
        player2 = self.create_player('Test Player2', '123456')

        # Create a new game
        new_game = self.create_game(player1.id)

        # Set each player as a participant in the game
        player1.current_game_id = new_game.id
        player2.current_game_id = new_game.id
        new_game.player2_id = player2.id
        db.session.commit()

        # [Play moves leading to a draw...]
        # Assuming a 3x3 board, a draw can be achieved with the following moves:
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 1), (1, 0), (1, 2),
            (2, 1), (2, 0), (2, 2)
        ]
        players = [player1.id, player2.id]

        for idx, move in enumerate(moves):
            player_id = players[idx % 2]
            player_token = create_access_token(player_id)
            move_response = self.client.post('/api/move',
                                             json={'row': move[0], 'col': move[1], 'gameId': new_game.id},
                                             headers={'Authorization': f'Bearer {player_token}'})

            assert move_response.status_code == 200, f"Move failed at step {idx} by player {player_id}, response: {move_response.get_data(as_text=True)}"

            # Optionally, fetch and log the current game state after each move for debugging
            game_state = db.session.get(Game, new_game.id)
            logging.info(f"Step {idx}, Game State: {game_state.current_player}, Board: {game_state.board_state}")

        # Check final state of the game
        updated_game = db.session.get(Game, new_game.id)
        assert updated_game.game_over is True, "Game should be over."
        assert updated_game.winner == 'D', "Game should be a draw."
        # Fetch the updated player states to check ELO rating change
        updated_player1 = db.session.get(Player, player1.id)
        updated_player2 = db.session.get(Player, player2.id)
        self.assertEqual(updated_player1.elo_rating, 1000)
        self.assertEqual(updated_player2.elo_rating, 1000)

    @allure.story('Test Move by Non-Participant')
    def test_move_by_non_participant(self):
        # Create players
        player1 = self.create_player('Test Player1', '123456')

        # Create a new game
        new_game = self.create_game(player1.id)

        # Set each player as a participant in the game
        player1.current_game_id = new_game.id
        db.session.commit()

        # Create JWT tokens for players
        non_participant = self.create_player('Non Participant', '123456')
        token_non_participant = create_access_token(non_participant.id)

        # Attempt to make a move by a player not in the game
        move_response = self.client.post('/api/move',
                                         json={'row': 0, 'col': 0, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token_non_participant}'})
        assert move_response.status_code == 400

    @allure.story('Test Move Out of Turn')
    def test_move_out_of_turn(self):
        # Create players
        player1 = self.create_player('Test Player1', '123456')
        player2 = self.create_player('Test Player2', '123456')

        # Create a new game
        new_game = self.create_game(player1.id)

        # Set each player as a participant in the game
        player1.current_game_id = new_game.id
        player2.current_game_id = new_game.id
        new_game.player2_id = player2.id
        db.session.commit()

        # Create JWT tokens for players
        token1 = create_access_token(player1.id)
        # Player 1 makes a move
        self.client.post('/api/move',
                         json={'row': 0, 'col': 0, 'gameId': new_game.id},
                         headers={'Authorization': f'Bearer {token1}'})

        # Player 1 attempts to make another move out of turn
        move_response = self.client.post('/api/move',
                                         json={'row': 1, 'col': 0, 'gameId': new_game.id},
                                         headers={'Authorization': f'Bearer {token1}'})
        assert move_response.status_code == 400


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
