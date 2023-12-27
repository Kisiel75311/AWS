# backend/game/TicTacToe.py
from models import db
from models.game_model import Game


class TicTacToe:
    def __init__(self, game_id=None):
        self.id = game_id  # Identyfikator gry z bazy danych
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.switch_player()
            # Aktualizacja stanu gry w bazie danych
            game_record = db.session.get(Game, self.id)
            game_record.board_state = self.get_board_state()
            game_record.current_player = self.current_player
            db.session.commit()
            return True
        return False

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ''

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        return None if '' in self.board[0] or '' in self.board[1] or '' in self.board[2] else "Draw"

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        # Zaktualizuj stan gry w bazie danych
        game_record = db.session.get(Game, self.id)
        game_record.board_state = self.get_board_state()
        game_record.current_player = self.current_player
        game_record.game_over = False
        game_record.winner = None
        db.session.commit()

    def get_board_state(self):
        return ''.join(''.join(row) for row in self.board)

    def set_board_state_from_string(self, state_str):
        self.board = [list(state_str[i:i + 3]) for i in range(0, 9, 3)]

    def switch_player(self):
        if self.check_winner() or self.is_full():
            self.game_state = 0
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_board_as_2d_array(self):
        return self.board
