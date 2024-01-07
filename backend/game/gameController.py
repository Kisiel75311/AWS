# backend/game/gameController.py
# from .TicTacToe import TicTacToe
from models.game_model import Game
from models import db
from contextlib import contextmanager

from models.player_model import Player
from exceptions import GameError


class GameController:

    def get_game(self, game_id):
        """Get game from the database and create a new game instance."""
        game_record = db.session.query(Game).filter_by(id=game_id).first()
        if game_record:
            # new_game = TicTacToe(game_id=game_id)
            new_game = db.session.query(Game).filter_by(id=game_id).first()
            new_game.set_board_state_from_string(game_record.board_state)
            new_game.current_player = game_record.current_player
            return new_game
        return None

    def create_new_game(self, player_id):
        player = db.session.get(Player, player_id)
        self._handle_player_game_change(player, None)  # Handle existing game if any

        new_game = Game()
        game_record = Game(board_state=new_game.get_board_state(), current_player='X', winner=None, game_over=False,
                           player1_id=player_id)
        db.session.add(game_record)
        db.session.commit()

        player.current_game_id = game_record.id
        db.session.commit()

        return game_record.id, new_game.get_board_as_2d_array(), new_game.current_player

    def player_join_game(self, game_id, player_id):
        game = db.session.query(Game).filter_by(id=game_id).first()
        player = db.session.get(Player, player_id)
        self._handle_player_game_change(player, game_id)  # Handle existing game if any

        if not game.player1_id:
            game.player1_id = player_id
        elif not game.player2_id and game.player1_id != player_id:
            game.player2_id = player_id
        else:
            raise Exception("Game already has two players or player is trying to join the same game.")

        player.current_game_id = game_id
        db.session.commit()

        return "Player joined the game", game.board_state, game.current_player

    def play_move(self, game_id, row, col, player_id):
        game_record = db.session.get(Game, game_id)
        if not game_record or game_record.game_over:
            raise GameError("Cannot play in a completed game.", 400)

        if player_id not in [game_record.player1_id, game_record.player2_id]:
            raise GameError(f"Player is not a participant of this game: {player_id, game_id}", 400)
        game = self.get_game(game_id)
        if not game:
            raise GameError("Game not found.", 404)

        if game.current_player not in ['X', 'O']:
            raise GameError("Invalid turn.", 400)

        if not game.make_move(row, col):
            raise GameError("Invalid move.", 400)

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

        if game_over:
            return f"Game over: {winner}", game.get_board_as_2d_array(), game.current_player
        else:
            return "Move played successfully.", game.get_board_as_2d_array(), game.current_player

    def reset_game(self, game_id, player_id):
        game_record = db.session.query(Game).filter_by(id=game_id).first()
        if not game_record:
            return "Game not found.", None, None

        if player_id not in [game_record.player1_id, game_record.player2_id]:
            return "Player is not a participant of this game.", None, None

        game = self.get_game(game_id)
        if not game:
            return "Game not found.", None, None

        game.reset_board()
        game_record.board_state = game.get_board_state()
        game_record.current_player = game.current_player
        game_record.game_over = False
        game_record.winner = None

        db.session.commit()
        return "Game reset.", game.get_board_as_2d_array(), 'X'

    def _handle_player_game_change(self, player, game_id):
        if player.current_game_id:
            current_game = db.session.get(Game, player.current_game_id)
            if current_game.player1_id == player.id:
                current_game.player1_id = None
            elif current_game.player2_id == player.id:
                current_game.player2_id = None

            player.current_game_id = None
            db.session.commit()
