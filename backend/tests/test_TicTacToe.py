import unittest
from unittest.mock import patch, MagicMock
from game.TicTacToe import TicTacToe
import allure

@allure.feature('TicTacToe Game')
class TestTicTacToe(unittest.TestCase):

    @patch('game.TicTacToe.db.session', new_callable=MagicMock)
    def setUp(self, mock_db):
        self.mock_db = mock_db
        self.mock_game = MagicMock()
        self.mock_db.get.return_value = self.mock_game
        self.game = TicTacToe()

    @allure.story('Valid Move')
    def test_is_valid_move_valid(self):
        valid_move = self.game.is_valid_move(0, 0)
        self.assertTrue(valid_move)

    @allure.story('Invalid Move')
    def test_is_valid_move_invalid(self):
        self.game.board[0][0] = 'X'
        invalid_move = self.game.is_valid_move(0, 0)
        self.assertFalse(invalid_move)

    @allure.story('Out of Bounds Move')
    def test_is_valid_move_out_of_bounds(self):
        invalid_move = self.game.is_valid_move(4, 4)
        self.assertFalse(invalid_move)

    @allure.story('Check for Winner')
    def test_check_winner_no_winner(self):
        winner = self.game.check_winner()
        self.assertIsNone(winner)

    @allure.story('Make Move')
    def test_make_move_invalid_move(self):
        self.game.board[0][0] = 'X'
        move_made = self.game.make_move(0, 0)
        self.assertFalse(move_made)
        self.mock_db.commit.assert_not_called()

    @allure.story('Move Out of Bounds')
    def test_make_move_out_of_bounds(self):
        move_made = self.game.make_move(4, 4)
        self.assertFalse(move_made)
        self.mock_db.commit.assert_not_called()

    @allure.story('Get Board State')
    def test_get_board_state_empty_board(self):
        expected_state = ''
        self.assertEqual(self.game.get_board_state(), expected_state)

    @allure.story('Set Board State')
    def test_set_board_state_from_string(self):
        self.game.set_board_state_from_string('XXX      ')
        self.assertEqual(self.game.board[0], list('XXX'))
        self.assertEqual(self.game.board[1], list('   '))
        self.assertEqual(self.game.board[2], list('   '))

    @allure.story('Switch Player')
    def test_switch_player(self):
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'O')
