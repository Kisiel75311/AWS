# backend/api/game_api.py
from flask import Blueprint, request, jsonify
from services.game_service import GameService
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.player_model import Player

game_blueprint = Blueprint('api', __name__)
game_service = GameService()


@game_blueprint.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    return response


@game_blueprint.route('/start', methods=['GET'])
@jwt_required()
def start_game():
    user_id = get_jwt_identity()  # Extracting user_id from the JWT token

    # Check if user_id exists in the database
    user = Player.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    try:
        game_id, board_state, current_player = game_service.create_new_game(user_id)
        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': 'New game started.',
            'gameId': game_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@game_blueprint.route('/move', methods=['POST'])
@jwt_required()
def make_move():
    user_id = request.args.get('user_id')
    game_id = request.args.get('gameId')
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')

    if not isinstance(row, int) or not isinstance(col, int) or not isinstance(game_id, int):
        return jsonify({'error': 'Invalid input.'}), 400

    try:
        result, board_state, current_player = game_service.play_move(game_id, row, col, user_id)
        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': result,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@game_blueprint.route('/reset', methods=['GET'])
@jwt_required()
def reset_game():
    user_id = request.args.get('user_id')
    game_id = request.args.get('gameId')

    if game_id is None:
        return jsonify({'error': 'Game ID is required.'}), 400

    try:
        game_id = int(game_id)
        result, board_state, current_player = game_service.reset_game(game_id, user_id)
        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': result
        })
    except ValueError:
        return jsonify({'error': 'Invalid Game ID.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@game_blueprint.route('/all_games', methods=['GET'])
def get_all_games():
    try:
        games = game_service.get_all_games()
        return jsonify({
            'games': games
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400