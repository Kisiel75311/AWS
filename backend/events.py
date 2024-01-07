# events.py
from flask_socketio import SocketIO, emit, join_room
from flask_jwt_extended import decode_token
from models import db
from models.game_model import Game
from services.game_service import GameService
import logging



def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print("Client connected")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")

    @socketio.on('start_game')
    def handle_start_game(data):
        token = data['token']
        user_id = decode_token(token)['identity']

        # Rozpocznij nową grę
        game_id, board_state, current_player = GameService.create_new_game(user_id)

        # Dodaj gracza do pokoju gry
        join_room(game_id)

        emit('game_updated', {'gameId': game_id, 'boardState': board_state, 'currentPlayer': current_player},
             to=game_id)

    @socketio.on('make_move')
    def handle_make_move(data):
        try:
            game_id = data['gameId']
            row = data['row']
            col = data['col']
            token = data['token']
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']

            # Wykonanie ruchu w grze
            message, board_state, current_player = GameService.play_move(game_id, row, col, user_id)

            # Logowanie przed emisją eventu
            logging.info(f"Emitting game_updated for game {game_id}: boardState={board_state}, currentPlayer={current_player}, message={message}")

            # Emit aktualizacji gry do wszystkich uczestników
            emit('game_updated', {'boardState': board_state, 'currentPlayer': current_player, 'message': message},
                 room=game_id)

        except KeyError as e:
            emit('error', {'message': f'Missing data in request: {e}'})
            logging.error(f"KeyError in handle_make_move: {e}")
        except Exception as e:
            emit('error', {'message': str(e)})
            logging.error(f"Exception in handle_make_move: {e}")


    @socketio.on('join_game')
    def handle_join_game(data):
        try:
            game_id = data['gameId']
            # user_id = data['userId']  # Pobieranie user_id z danych przesłanych przez klienta
            token = data['token']
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            # Dołączanie do gry
            message, board_state, current_player = GameService.player_join_game(game_id, user_id)
            join_room(game_id)
            emit('game_updated', {'boardState': board_state, 'currentPlayer': current_player, 'message': message},
                 room=game_id)

        except KeyError as e:
            emit('error', {'message': f'Missing data in request: {e}'})
        except Exception as e:
            emit('error', {'message': str(e)})

    @socketio.on('reset_game')
    def handle_reset_game(data):
        game_id = data['gameId']
        # user_id = data['userId']
        token = data['token']
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']

        # Resetuj grę
        message, board_state, current_player = GameService.reset_game(game_id, user_id)
        emit('game_updated', {'boardState': board_state, 'currentPlayer': current_player, 'message': message},
             to=game_id)
