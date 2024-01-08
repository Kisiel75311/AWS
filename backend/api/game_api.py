# backend/api/game_api.py
from flask import Blueprint, request, jsonify
from services.game_service import GameService
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.player_model import Player
from models import db

from models.game_model import Game

from exceptions import GameError

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
    user = db.session.get(Player, user_id)
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
    user_id = get_jwt_identity()  # Extracting user_id from the JWT token
    data = request.get_json()

    # Extract game_id, row, and col from JSON body
    game_id = data.get('gameId')
    row = data.get('row')
    col = data.get('col')

    # Validate inputs
    if not all([isinstance(game_id, int), isinstance(row, int), isinstance(col, int)]):
        return jsonify({'error': 'Invalid input.'}), 400

    # Get the player
    player = db.session.query(Player).filter_by(id=user_id).first()

    if not player:
        return jsonify({'error': 'Player not found.'}), 404

    if player.current_game_id != game_id:
        return jsonify({'error': 'Player is not part of the game.'}), 400

    try:
        result, board_state, current_player = game_service.play_move(game_id, row, col, user_id)
        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': result,
            'gameId': game_id,
        })
    except GameError as e:
        # Obsługa wyjątku GameError
        response = e.to_dict()
        return jsonify(response), e.status_code
    except Exception as e:
        # Obsługa innych wyjątków
        return jsonify({'error': str(e)}), 500


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
            'message': result,
            'gameId': game_id
        })
    except ValueError:
        return jsonify({'error': 'Invalid Game ID.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@game_blueprint.route('/join', methods=['POST'])
@jwt_required()
def join_game():
    user_id = get_jwt_identity()  # Extracting user_id from the JWT token
    data = request.get_json()
    game_id = data.get('gameId')

    if not game_id:
        return jsonify({'error': 'Game ID is required.'}), 400

    # Check if the game exists
    game = db.session.get(Game, game_id)
    if not game:
        return jsonify({'error': 'Game not found.'}), 404

    try:
        result, board_state, current_player = game_service.player_join_game(game_id, user_id)
        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': result,
            'gameId': game_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@game_blueprint.route('/all_games', methods=['GET'])
def get_all_games():
    try:
        games = Game.query.all()
        games_data = [game.to_dict() for game in games]  # Corrected line
        return jsonify({
            'games': games_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@game_blueprint.route('/game/<int:game_id>', methods=['GET'])
@jwt_required()
def get_game(game_id):
    # Sprawdź, czy gra istnieje
    game = db.session.get(Game, game_id)
    if not game:
        return jsonify({'error': 'Game not found.'}), 404

    # Sprawdź, czy użytkownik jest uczestnikiem gry
    user_id = get_jwt_identity()
    if user_id not in [game.player1_id, game.player2_id]:
        return jsonify({'error': 'User is not a participant of this game.'}), 403

    try:
        board_state = GameService.get_board_as_2d_array(game.board_state)
        return jsonify({
            'gameId': game.id,
            'boardState': board_state,
            'currentPlayer': game.current_player,
            'gameOver': game.game_over,
            'winner': game.winner
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@game_blueprint.route('/join_random', methods=['POST'])
@jwt_required()
def join_random_game():
    user_id = get_jwt_identity()
    game = GameService.join_random_game(user_id)
    return jsonify({
        'message': 'Joined game',
        'gameId': game.id,
        'boardState': GameService.get_board_as_2d_array(game.board_state),
        'currentPlayer': game.current_player
    })


@game_blueprint.route('/leave', methods=['POST'])
@jwt_required()
def leave_game():
    user_id = get_jwt_identity()
    game = GameService.leave_game(user_id)
    return jsonify({
        'message': 'Left game',
        'gameId': game.id,
        'boardState': GameService.get_board_as_2d_array(game.board_state),
        'currentPlayer': game.current_player
    })


@game_blueprint.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        players = Player.query.order_by(Player.elo.desc()).all()
        players_data = [player.to_dict() for player in players]
        return jsonify({
            'players': players_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
