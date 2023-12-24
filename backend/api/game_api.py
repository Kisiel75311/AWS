# backend/api/game_api.py

from flask import Blueprint, request, jsonify
from game.gameController import GameController

game_blueprint = Blueprint('game', __name__)
game_controller = GameController()

@game_blueprint.route('/start', methods=['GET'])
def start_game():
    game_controller.reset_game()
    board_state = game_controller.board.get_board_as_2d_array()
    current_player = game_controller.get_current_player().symbol
    return jsonify({'message': 'Nowa gra rozpoczęta.', 'state': board_state, 'current_player': current_player})

@game_blueprint.route('/move', methods=['POST'])
def make_move():
    data = request.json
    row = data.get('row')
    col = data.get('col')

    if row is None or col is None:
        return jsonify({'error': 'Brakujące parametry ruchu (row, col).'}), 400

    result = game_controller.play_move(row, col)
    board_state = game_controller.board.get_board_as_2d_array()
    current_player = game_controller.get_current_player().symbol
    return jsonify({'message': result, 'state': board_state, 'current_player': current_player})

@game_blueprint.route('/reset', methods=['GET'])
def reset_game():
    game_controller.reset_game()
    board_state = game_controller.board.get_board_as_2d_array()
    current_player = game_controller.get_current_player().symbol
    return jsonify({'message': 'Gra została zresetowana.', 'state': board_state, 'current_player': current_player})
