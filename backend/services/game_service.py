# backend/services/game_service.py
from game.gameController import GameController
from models.player_model import Player
from models.game_model import Game
from models import db


class GameService:
    def __init__(self):
        self.game_controller = GameController()

    def create_new_game(self, player_id):
        # Sprawdź, czy gracz istnieje
        player = db.session.get(Player, player_id)
        if not player:
            raise Exception("Player not found.")

        # Utwórz nową grę za pomocą GameController i zaktualizuj gracza
        game_id, board, current_player = self.game_controller.create_new_game(player_id)
        return game_id, board, current_player

    def play_move(self, game_id, row, col, player_id):
        # Sprawdź, czy gracz istnieje i jest przypisany do gry
        player = db.session.get(Player, player_id)
        if not player or player.current_game_id != game_id:
            raise Exception("Player not found or not part of the game.")

        # Wykonaj ruch za pomocą GameController
        message, board, current_player = self.game_controller.play_move(game_id, row, col, player_id)
        return message, board, current_player

    def reset_game(self, game_id, player_id):
        # Sprawdź, czy gracz istnieje i jest przypisany do gry
        player = db.session.get(Player, player_id)
        if not player or player.current_game_id != game_id:
            raise Exception("Player not found or not part of the game.")

        # Zresetuj grę za pomocą GameController
        message, board, current_player = self.game_controller.reset_game(game_id, player_id)
        return message, board, current_player

    def player_join_game(self, game_id, player_id):
        game = db.session.get(Game, game_id)
        if not game:
            raise Exception("Game not found.")

        # Check if the game is already full
        if game.player1_id and game.player2_id:
            raise Exception("Game is already full.")

        if not game.player1_id:
            game.player1_id = player_id
        elif not game.player2_id:
            game.player2_id = player_id

        db.session.commit()

        # Return game state, message, etc.
        return "Player joined", game.board_state, game.current_player

    def get_all_games(self):
        return Game.query.all()
