# backend/services/game_service.py
import logging

from models.player_model import Player
from models.game_model import Game
from models import db
from exceptions import PlayerNotFoundException, GameNotFoundException, InvalidMoveException, NotYourTurnException, GameFullException, GameError

class GameService:
    board_size = 3

    @staticmethod
    def create_new_game(player_id):
        player = db.session.get(Player, player_id)
        if not player:
            raise PlayerNotFoundException("Player not found.")

        # Usuń gracza z obecnej gry, jeśli jest w jakiejś
        if player.current_game_id:
            current_game = db.session.get(Game, player.current_game_id)
            if current_game:
                if current_game.player1_id == player_id:
                    current_game.player1_id = None
                elif current_game.player2_id == player_id:
                    current_game.player2_id = None
                db.session.commit()

        # Zmieniamy inicjalizację board_state na 9 spacji
        board_state = '.' * (GameService.board_size ** 2)
        logging.info(f"Initial board_state: {board_state}")

        new_game = Game(board_state=board_state, current_player='X', winner=None, game_over=False, player1_id=player_id)
        db.session.add(new_game)
        db.session.commit()

        player.current_game_id = new_game.id
        db.session.commit()

        logging.info(f"New game created with board_state: {new_game.board_state}")

        GameService.cleanup_empty_games()
        return new_game.id, GameService.get_board_as_2d_array(new_game.board_state), new_game.current_player


    @staticmethod
    def play_move(game_id, row, col, player_id):
        player = db.session.get(Player, player_id)
        game = db.session.get(Game, game_id)

        if not player:
            raise PlayerNotFoundException("Player not found.")

        if not game:
            raise GameNotFoundException("Game not found.")

        if player.current_game_id != game_id:
            raise PlayerNotFoundException(f"Player {player_id} is not part of the game {game_id}.")

        # Sprawdzenie, czy gra ma już obu graczy
        if not game.player1_id or not game.player2_id:
            raise GameError("Game is not yet full.", 400)

        # Sprawdzenie, czy jest kolej tego gracza
        if game.current_player_id != player_id:
            raise GameError("Not your turn.", 400)

        if not GameService.is_valid_move(game.board_state, row, col):
            raise GameError("Invalid move.", 400)

        # if player.id != game.current_player_id:
        #     raise GameError("Invalid turn.", 400)

        # Aktualizacja planszy
        board_list = list(game.board_state)
        board_list[row * GameService.board_size + col] = game.current_player
        game.board_state = ''.join(board_list)

        # Zmiana aktualnego gracza
        next_player_id, next_player_symbol = GameService.switch_player(player.id, game.id)
        game.current_player = next_player_symbol
        game.current_player_id = next_player_id

        winner = GameService.check_winner(game.board_state)
        if winner:

            game.game_over = True
            game.winner = winner

        db.session.commit()
        return "Move played successfully.", GameService.get_board_as_2d_array(game.board_state), game.current_player

    @staticmethod
    def reset_game(game_id, player_id):
        game = db.session.get(Game, game_id)
        player = db.session.get(Player, player_id)
        if not game:
            raise GameNotFoundException("Game not found.")

        if player.current_game_id != game_id:
            raise PlayerNotFoundException(f"Player {player_id} is not part of the game {game_id}.")

        game.board_state = '.' * (GameService.board_size ** 2)
        game.current_player = 'X'
        game.game_over = False
        game.winner = None
        db.session.commit()
        return "Game reset.", GameService.get_board_as_2d_array(game.board_state), 'X'

    @staticmethod
    def player_join_game(game_id, player_id):
        game = db.session.get(Game, game_id)
        player = db.session.get(Player, player_id)

        if not game:
            raise GameNotFoundException("Game not found.")
        # Usuń gracza z obecnej gry, jeśli jest w jakiejś
        if player.current_game_id:
            current_game = db.session.get(Game, player.current_game_id)
            if current_game:
                if current_game.player1_id == player_id:
                    current_game.player1_id = None
                elif current_game.player2_id == player_id:
                    current_game.player2_id = None
                db.session.commit()
        if game.player1_id and game.player2_id:
            raise GameFullException("Game is already full.")
        if player_id in [game.player1_id, game.player2_id]:
            raise Exception("Player is already in the game.")

        if not game.player1_id:
            game.player1_id = player_id
        elif not game.player2_id:
            game.player2_id = player_id

        player.current_game_id = game_id
        db.session.commit()

        board_state2d = GameService.get_board_as_2d_array(game.board_state)

        GameService.cleanup_empty_games()
        return "Player joined", board_state2d, game.current_player

    @staticmethod
    def check_winner(board_state):
        board = GameService.get_board_as_2d_array(board_state)

        # Sprawdzanie wierszy i kolumn
        for i in range(GameService.board_size):
            if board[i][0] == board[i][1] == board[i][2] != '.':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '.':
                return board[0][i]

        # Sprawdzanie przekątnych
        if board[0][0] == board[1][1] == board[2][2] != '.':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '.':
            return board[0][2]

        # Sprawdzenie, czy plansza jest pełna, oznacza remis
        if all(cell != '.' for row in board for cell in row):
            return "Draw"

        return None  # Brak zwycięzcy lub remisu

    @staticmethod
    def is_valid_move(board_state, row, col):
        try:
            if 0 <= row < GameService.board_size and 0 <= col < GameService.board_size:
                board = GameService.get_board_as_2d_array(board_state)
                logging.info(f"board_state={board_state}, board={board}, len(board_state)={len(board_state)}")
                return board[row][col] == '.'  # Zmiana z ' ' na '.'
            else:
                return False
        except IndexError as e:
            logging.error(f"IndexError in is_valid_move: row={row}, col={col}, error={e}")
            return False

    @staticmethod
    def get_board_as_2d_array(board_state):
        # Ta metoda pozostaje bez zmian, ponieważ zakłada już, że board_state jest ciągiem znaków
        return [list(board_state[i:i + GameService.board_size]) for i in
                range(0, len(board_state), GameService.board_size)]

    @staticmethod
    def get_board_state(board):
        return '.'.join('.'.join(row) for row in board)

    @staticmethod
    def switch_player(current_player_id, game_id):
        game = db.session.get(Game, game_id)
        if not game:
            raise GameNotFoundException("Game not found.")

        # Sprawdzenie czy gra się zakończyła
        if GameService.check_winner(game.board_state) or GameService.is_full(game.board_state):
            return None, None  # Gra zakończona

        # Ustalenie, który gracz ma teraz ruch
        if current_player_id == game.player1_id:
            return game.player2_id, 'O'
        else:
            return game.player1_id, 'X'

    @staticmethod
    def is_full(board_state):
        return '.' not in board_state

    @staticmethod
    def cleanup_empty_games():
        empty_games = Game.query.filter(Game.player1_id.is_(None), Game.player2_id.is_(None)).all()
        for game in empty_games:
            db.session.delete(game)
        db.session.commit()