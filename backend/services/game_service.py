# backend/services/game_service.py
from game.gameController import GameController

class GameService:
    def __init__(self):
        self.game_controller = GameController()

    def create_new_game(self):
        game_id, board_state, current_player = self.game_controller.create_new_game()
        return game_id, board_state, current_player

    def play_move(self, game_id, row, col):
        result, board_state, current_player = self.game_controller.play_move(game_id, row, col)
        return result, board_state, current_player

    def reset_game(self, game_id):
        result, board_state, current_player = self.game_controller.reset_game(game_id)
        return result, board_state, current_player
