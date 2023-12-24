#backend/game/board.py
class Board:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player.symbol
            return True
        return False

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ''

    def check_winner(self):
        # Sprawdzanie wierszy, kolumn i przekątnych
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        return None

    def is_full(self):
        return all(self.board[row][col] != '' for row in range(3) for col in range(3))

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def get_board_state(self):
        return ''.join(''.join(row) for row in self.board)

    def get_board_as_2d_array(self):
        return self.board