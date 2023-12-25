from flask import Blueprint, request, jsonify, session
from game.gameController import GameController

game_blueprint = Blueprint('api', __name__)
game_controller = GameController()  # Tworzenie pojedynczego kontrolera gry

@game_blueprint.route('/start', methods=['GET'])
def start_game():
    game_id, board_state, current_player = game_controller.create_new_game()

    # Sprawdzenie, czy game_id zostało poprawnie utworzone
    if game_id is None:
        return jsonify({'error': 'Nie udało się utworzyć nowej gry.'}), 500

    session['game_id'] = game_id
    session.modified = True
    return jsonify({
        'boardState': board_state,
        'currentPlayer': current_player,
        'message': 'Nowa gra rozpoczęta.',
        'gameId': game_id
    })


@game_blueprint.route('/move', methods=['POST'])
def make_move():
    session_string = str(session.get('game_id'))

    if "game_id" in session:
        game_id = session.get('game_id')
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')

        result, board_state, current_player = game_controller.play_move(game_id, row, col)
        if not board_state:
            return jsonify({'error': result}), 400  # Błąd, np. nieprawidłowy ruch

        return jsonify({
            'boardState': board_state,
            'currentPlayer': current_player,
            'message': result,
        })
    else:
        return jsonify({'error': 'Gra nie została jeszcze rozpoczęta. session.get: ' + session_string}), 400


@game_blueprint.route('/reset', methods=['GET'])
def reset_game():
    game_id = session.get('game_id')
    if not game_id:
        return jsonify({'error': 'Gra nie została jeszcze rozpoczęta.'}), 400

    result, board_state, current_player = game_controller.reset_game(game_id)
    if not board_state:
        return jsonify({'error': result}), 400  # Błąd, np. gra nie została znaleziona
    return jsonify({
        'boardState': board_state,
        'currentPlayer': current_player,
        'message': result
    })
