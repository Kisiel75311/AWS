# gameController.py

from .board import Board
from .player import Player
from api.models import db, Game

class GameController:
    def __init__(self):
        self.board = Board()
        self.players = [Player('X'), Player('O')]
        self.current_player_index = 0
        self.game_record = None

    def start_new_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.game_record = Game(board_state=self.board.get_board_state(), current_player='X')
        db.session.add(self.game_record)
        db.session.commit()

    def play_move(self, row, col):
        player = self.players[self.current_player_index]
        if self.board.make_move(row, col, player):
            self.update_game_record()
            winner = self.board.check_winner()
            if winner or self.board.is_full():
                return "Game Over: Winner is " + winner if winner else "Game Over: It's a Draw"
            self.current_player_index = (self.current_player_index + 1) % 2
            return "Move accepted"
        return "Invalid move"

    def update_game_record(self):
        if self.game_record:
            self.game_record.board_state = self.board.get_board_state()
            self.game_record.current_player = self.players[self.current_player_index].symbol
            db.session.commit()

    def reset_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.update_game_record()

    def get_current_player(self):
        return self.players[self.current_player_index]
