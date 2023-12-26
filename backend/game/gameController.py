# backend/game/gameController.py
from .TicTacToe import TicTacToe
from models.game_model import Game, db
from contextlib import contextmanager


class GameController:
    def __init__(self):
        self.games = {}

    def create_new_game(self):
        new_game = TicTacToe()
        game_record = Game(board_state=new_game.get_board_state(), current_player='X', winner=None, game_over=False)
        db.session.add(game_record)
        db.session.commit()
        self.games[game_record.id] = new_game
        return game_record.id, new_game.get_board_as_2d_array(), new_game.current_player

    def play_move(self, game_id, row, col):
        game_record = db.session.get(Game, game_id)
        if not game_record or game_record.game_over:
            return "Nie można grać w zakończoną grę.", None, None

        game = self.games.get(game_id)
        if not game:
            return "Gra nie została znaleziona.", None, None

        if not game.make_move(row, col):
            return "Nieprawidłowy ruch.", None, None

        winner = game.check_winner()
        game_record.board_state = game.get_board_state()
        game_record.current_player = game.current_player

        game_over = False
        if winner:
            game_over = True
            game_record.game_over = True
            game_record.winner = winner
        elif game.is_full():
            game_over = True
            game_record.game_over = True
            game_record.winner = "Draw"

        db.session.commit()
        return ("Ruch wykonany pomyślnie.", game.get_board_as_2d_array(), game.current_player) if not game_over else \
            ("Gra zakończona: " + winner, game.get_board_as_2d_array(), game.current_player)

    def reset_game(self, game_id):
        game_record = db.session.get(Game, game_id)
        if not game_record:
            return "Gra nie została znaleziona.", None, None

        game = self.games.get(game_id)
        if not game:
            return "Gra nie została znaleziona.", None, None

        game.reset_board()
        game_record.board_state = game.get_board_state()
        game_record.current_player = game.current_player
        game_record.game_over = False
        game_record.winner = None

        db.session.commit()
        return "Gra została zresetowana.", game.get_board_as_2d_array(), 'X'
