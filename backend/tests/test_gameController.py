import unittest
from unittest.mock import Mock, patch
from game.gameController import GameController

from exceptions import GameError
import allure


class GameControllerTest(unittest.TestCase):

    def setUp(self):
        self.controller = GameController()

    @patch('game.gameController.db.session')
    def test_get_game(self, mock_db):
        mock_db.query.return_value.filter_by.return_value.first.return_value = Mock(board_state=' ',
                                                                                    current_player='X')
        game = self.controller.get_game(1)
        self.assertIsNotNone(game)
        self.assertEqual(game.current_player, 'X')

    @patch('game.gameController.db.session')
    def test_create_new_game_player_not_found(self, mock_db):
        mock_db.get.return_value = None

        with self.assertRaises(AttributeError):
            self.controller.create_new_game(1)

    @patch('game.gameController.db.session')
    def test_player_join_game_two_players(self, mock_db):
        mock_game = Mock(player1_id=1, player2_id=None)
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_game
        mock_db.get.return_value = Mock(id=2)

        with self.assertRaises(Exception):
            self.controller.player_join_game(1, 1)

    @patch('game.gameController.db.session')
    @patch('game.gameController.TicTacToe')
    @patch('game.gameController.Game')
    def test_play_move(self, mock_game_model, mock_tic_tac_toe, mock_db):
        # Konfiguracja mocka game_record
        game_id = 1
        mock_game_record = Mock()
        mock_game_record.id = game_id
        mock_game_record.game_over = False
        mock_game_record.player1_id = 1
        mock_game_record.player2_id = 2
        mock_game_record.current_player = 'X'
        mock_game_record.board_state = ''

        # Konfiguracja mocka game_instance
        mock_game_instance = mock_tic_tac_toe()
        mock_game_instance.current_player = 'X'
        mock_game_instance.make_move.return_value = True
        mock_game_instance.check_winner.return_value = None  # Zwróć None, aby wskazać, że nie ma jeszcze zwycięzcy
        mock_game_instance.is_full.return_value = False  # Dodatkowo upewnij się, że gra nie jest pełna

        mock_db.get.return_value = mock_game_record
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_game_record
        self.controller.get_game = Mock(return_value=mock_game_instance)

        try:
            message, _, _ = self.controller.play_move(1, 0, 0, 1)
            self.assertEqual(message, "Move played successfully.")
        except GameError as e:
            self.fail(
                f"We didn't expect a GameError here: {str(e.message)}")  # Zwróć uwagę na zmieniony str(e) na str(e.message)

        # Sprawdzamy, czy zwrócona wiadomość jest zgodna z oczekiwaniami
        self.assertEqual(message, "Move played successfully.")

    @patch('game.gameController.db.session')
    def test_reset_game(self, mock_db):
        # Ustawienie atrybutu board_state na ciąg znaków reprezentujący stan planszy
        mock_game_record = Mock(player1_id=1, player2_id=2, board_state='', current_player='X')
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_game_record
        message, _, current_player = self.controller.reset_game(1, 1)
        self.assertEqual(message, "Game reset.")
        self.assertEqual(current_player, 'X')

    @patch('game.gameController.db.session')
    def test_get_game_not_found(self, mock_db):
        mock_db.query.return_value.filter_by.return_value.first.return_value = None
        game = self.controller.get_game(1)
        self.assertIsNone(game)


    @patch('game.gameController.db.session')
    def test_player_join_game_not_found(self, mock_db):
        mock_db.query.return_value.filter_by.return_value.first.return_value = None
        mock_db.get.return_value = None

        with self.assertRaises(AttributeError):
            self.controller.player_join_game(1, 1)

    @patch('game.gameController.db.session')
    @patch('game.gameController.GameController.get_game')
    def test_play_move_game_over(self, mock_get_game, mock_db):
        mock_game_record = Mock(game_over=False, player1_id=1, player2_id=2, current_player='X')
        mock_db.get.return_value = mock_game_record
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_game_record

        mock_game_instance = Mock()
        mock_game_instance.current_player = 'X'
        mock_game_instance.make_move.return_value = True
        mock_game_instance.check_winner.return_value = 'X'  # Symulacja wygranej
        mock_game_instance.is_full.return_value = False
        mock_get_game.return_value = mock_game_instance

        try:
            message, _, _ = self.controller.play_move(1, 0, 0, 1)
            self.assertEqual(message, f"Game over: X")
        except GameError as e:
            self.fail(f"We didn't expect a GameError here: {e.message}")

    @patch('game.gameController.db.session')
    def test_reset_game_not_participant(self, mock_db):
        mock_game_record = Mock(player1_id=1, player2_id=2)
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_game_record

        message, _, _ = self.controller.reset_game(1, 3)
        self.assertEqual(message, "Player is not a participant of this game.")

    @patch('game.gameController.TicTacToe.make_move')
    @patch('game.gameController.db.session')
    def test_play_move_invalid_move(self, mock_make_move, mock_db):
        mock_make_move.return_value = False
        mock_game_record = Mock(game_over=False, player1_id=1, player2_id=2)
        mock_db.get.return_value = mock_game_record
        mock_db.query.return_value.filter_by.return_value.first.return_value = Mock(board_state=' ',
                                                                                    current_player='X')

        with self.assertRaises(GameError):
            self.controller.play_move(1, 0, 0, 1)


if __name__ == '__main__':
    unittest.main()
