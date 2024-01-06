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
        new_game = Game(board_state='', current_player='X', winner=None, game_over=False, player1_id=player1_id, player2_id=player2_id)
        db.session.add(new_game)
        db.session.commit()
        return new_game

    @allure.story('Test Start Game')
    def test_start_game(self):
        # Assume there is a valid player to make the requests
        player = self.create_player('Test Player', '123456')
        jwt_token = create_access_token(player.id)
        response = self.client.get('/api/start', headers={'Authorization': 'Bearer ' + jwt_token})
        self.assertEqual(200, response.status_code)

    @allure.story('Test Invalid Move')
    def test_invalid_move(self):
        # Tworzenie gracza
        player1 = self.create_player('Test Player1', '123456')

        # Tworzenie nowej gry
        new_game = self.create_game(player1.id)

        # Ustawienie gracza jako uczestnika gry
        player1.current_game_id = new_game.id
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

if __name__ == '__main__':
    unittest.main()
