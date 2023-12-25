from flask import Blueprint, request, jsonify
from game.gameController import GameController
from flask_cors import cross_origin

game_blueprint = Blueprint('api', __name__)
game_controller = GameController()


@game_blueprint.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    return response


@game_blueprint.route('/start', methods=['GET'])
# @cross_origin(supports_credentials=True)
def start_game():
    game_id, board_state, current_player = game_controller.create_new_game()
    if game_id is None:
        return jsonify({'error': 'Failed to create a new game.'}), 500

    return jsonify({
        'boardState': board_state,
        'currentPlayer': current_player,
        'message': 'New game started.',
        'gameId': game_id
    })


@game_blueprint.route('/move', methods=['POST'])
# @cross_origin(supports_credentials=True)
def make_move():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    game_id = data.get('gameId')

    if not isinstance(row, int) or not isinstance(col, int) or not isinstance(game_id, int):
        return jsonify({'error': 'Invalid input.'}), 400

    result, board_state, current_player = game_controller.play_move(game_id, row, col)
    if not board_state:
        return jsonify({'error': result}), 400

    return jsonify({
        'boardState': board_state,
        'currentPlayer': current_player,
        'message': result,
    })


@game_blueprint.route('/reset', methods=['GET'])
# @cross_origin(supports_credentials=True)
def reset_game():
    game_id = request.args.get('gameId')

    if game_id is None:
        return jsonify({'error': 'Game ID is required.'}), 400

    try:
        game_id = int(game_id)
    except ValueError:
        return jsonify({'error': 'Invalid Game ID.'}), 400

    result, board_state, current_player = game_controller.reset_game(game_id)
    if not board_state:
        return jsonify({'error': result}), 400

    return jsonify({
        'boardState': board_state,
        'currentPlayer': current_player,
        'message': result
    })
