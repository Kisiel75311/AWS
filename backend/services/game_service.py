# backend/services/game_service.py
import logging

from models.player_model import Player
from models.game_model import Game
from models import db
from exceptions import PlayerNotFoundException, GameNotFoundException, InvalidMoveException, NotYourTurnException, \
    GameFullException, GameError
import math


class GameService:
    BOARD_SIZE = 3
    EMPTY_CELL = '.'
    PLAYER_X = 'X'
    PLAYER_O = 'O'

    @staticmethod
    def create_new_game(player_id):
        logging.info(f"Fetching player with ID: {player_id}")
        player = db.session.get(Player, player_id)
        if not player:
            logging.error(f"No player found with ID: {player_id}")
            raise PlayerNotFoundException("Player not found.")

        # Usuń gracza z obecnej gry, jeśli jest w jakiejś
        GameService.remove_player_from_current_game(player_id)

        # Zmieniamy inicjalizację board_state na 9 spacji
        board_state = GameService.EMPTY_CELL * (GameService.BOARD_SIZE ** 2)
        logging.info(f"Initial board_state: {board_state}")

        new_game = Game(board_state=board_state, current_player=GameService.PLAYER_X, winner=None, game_over=False,
                        player1_id=player_id)
        db.session.add(new_game)
        db.session.commit()

        player.current_game_id = new_game.id
        db.session.commit()

        logging.info(f"New game created with board_state: {new_game.board_state}")

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

        # Aktualizacja planszy
        board_list = list(game.board_state)
        board_list[row * GameService.BOARD_SIZE + col] = game.current_player
        game.board_state = ''.join(board_list)

        # Zmiana aktualnego gracza
        next_player_id, next_player_symbol = GameService.switch_player(player.id, game.id)
        game.current_player = next_player_symbol
        game.current_player_id = next_player_id

        winner = GameService.check_winner(game.board_state)
        if winner:
            game.game_over = True
            game.winner = winner
            print(f"Game over, winner: {player.id}")
            GameService.end_game(game.id, player.id)  # Wywołaj end_game
            db.session.commit()
            return "Move played successfully, game ended.", GameService.get_board_as_2d_array(
                game.board_state), game.current_player
        else:
            # Kontynuuj grę, jeśli nie ma zwycięzcy
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

        game.board_state = GameService.EMPTY_CELL * (GameService.BOARD_SIZE ** 2)
        game.current_player = GameService.PLAYER_X
        game.game_over = False
        game.winner = None
        db.session.commit()
        return "Game reset.", GameService.get_board_as_2d_array(game.board_state), GameService.PLAYER_X

    @staticmethod
    def player_join_game(game_id, player_id):
        game = db.session.get(Game, game_id)
        player = db.session.get(Player, player_id)

        if not game:
            raise GameNotFoundException("Game not found.")

        # Usuń gracza z obecnej gry, jeśli jest w jakiejś
        GameService.remove_player_from_current_game(player_id)

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

        return "Player joined", board_state2d, game.current_player

    @staticmethod
    def check_winner(board_state):
        board = GameService.get_board_as_2d_array(board_state)

        # Sprawdzanie wierszy, kolumn i przekątnych
        for i in range(GameService.BOARD_SIZE):
            # Sprawdzanie wierszy
            if board[i][0] == board[i][1] == board[i][2] != GameService.EMPTY_CELL:
                return board[i][0]

            # Sprawdzanie kolumn
            if board[0][i] == board[1][i] == board[2][i] != GameService.EMPTY_CELL:
                return board[0][i]

        # Sprawdzanie przekątnych
        if board[0][0] == board[1][1] == board[2][2] != GameService.EMPTY_CELL:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != GameService.EMPTY_CELL:
            return board[0][2]

        # Sprawdzenie remisu - czy plansza jest pełna
        if all(cell != GameService.EMPTY_CELL for row in board for cell in row):
            return "D"

        return None  # Brak zwycięzcy lub remisu

    @staticmethod
    def is_valid_move(board_state, row, col):
        try:
            if 0 <= row < GameService.BOARD_SIZE and 0 <= col < GameService.BOARD_SIZE:
                board = GameService.get_board_as_2d_array(board_state)
                logging.info(f"board_state={board_state}, board={board}, len(board_state)={len(board_state)}")
                return board[row][col] == GameService.EMPTY_CELL  # Zmiana z ' ' na GameService.EMPTY_CELL
            else:
                return False
        except IndexError as e:
            logging.error(f"IndexError in is_valid_move: row={row}, col={col}, error={e}")
            return False

    @staticmethod
    def get_board_as_2d_array(board_state):
        # Ta metoda pozostaje bez zmian, ponieważ zakłada już, że board_state jest ciągiem znaków
        return [list(board_state[i:i + GameService.BOARD_SIZE]) for i in
                range(0, len(board_state), GameService.BOARD_SIZE)]

    @staticmethod
    def get_board_state(board):
        return GameService.EMPTY_CELL.join(GameService.EMPTY_CELL.join(row) for row in board)

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
            return game.player2_id, GameService.PLAYER_O
        else:
            return game.player1_id, GameService.PLAYER_X

    @staticmethod
    def is_full(board_state):
        return GameService.EMPTY_CELL not in board_state

    @staticmethod
    def cleanup_empty_games():
        empty_games = Game.query.filter(Game.player1_id.is_(None), Game.player2_id.is_(None)).all()
        for game in empty_games:
            db.session.delete(game)
        db.session.commit()

    @staticmethod
    def cleanup_finished_games():
        finished_games = Game.query.filter(Game.game_over.is_(True)).all()
        for game in finished_games:
            db.session.delete(game)
        db.session.commit()

    @staticmethod
    def remove_player_from_current_game(player_id):
        player = db.session.get(Player, player_id)
        if player and player.current_game_id:
            current_game = db.session.get(Game, player.current_game_id)
            if current_game:
                if current_game.player1_id == player_id:
                    current_game.player1_id = None
                elif current_game.player2_id == player_id:
                    current_game.player2_id = None
                db.session.commit()

    @staticmethod
    def join_random_game(player_id):
        available_game = Game.query.filter(
            ((Game.player1_id.is_(None)) | (Game.player2_id.is_(None))) &
            (Game.game_over.is_(False))
        ).first()

        if available_game:
            if available_game.player1_id is None:
                available_game.player1_id = player_id
            else:
                available_game.player2_id = player_id
            db.session.commit()
            return available_game
        else:
            return GameService.create_new_game(player_id)

    @staticmethod
    def leave_game(player_id):
        player = db.session.get(Player, player_id)
        if player and player.current_game_id:
            current_game = db.session.get(Game, player.current_game_id)
            if current_game:
                if current_game.player1_id == player_id:
                    current_game.player1_id = None
                elif current_game.player2_id == player_id:
                    current_game.player2_id = None
                db.session.commit()
                return current_game
        return None

    @staticmethod
    def end_game(game_id, winner_id):
        game = db.session.get(Game, game_id)
        if not game:
            raise GameNotFoundException("Game not found.")

        player1 = db.session.get(Player, game.player1_id)
        player2 = db.session.get(Player, game.player2_id)

        # check if elo rating is not None
        if player1.elo_rating is None or player2.elo_rating is None:
            raise GameError("Elo rating is None.")

        if not player1 or not player2:
            raise GameError("Both players must be present to end the game.")

        # Determine scores based on the winner
        if winner_id == game.player1_id:
            score1 = 1
        elif winner_id == game.player2_id:
            score1 = 0
        if game.winner == 'D':  # Draw
            score1 = 0.5

        # Calculate new ELO ratings
        new_rating1, new_rating2 = calculate_new_elo(player1.elo_rating, player2.elo_rating, score1)

        # Update ELO ratings
        player1.elo_rating = new_rating1
        player2.elo_rating = new_rating2

        db.session.commit()


def calculate_new_elo(rating1, rating2, score1):
    print(f"Calculating new ELO: rating1={rating1}, rating2={rating2}, score1={score1}")
    k = 30
    expected_score1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    expected_score2 = 1 - expected_score1
    score2 = 1 - score1

    new_rating1 = rating1 + k * (score1 - expected_score1)
    new_rating2 = rating2 + k * (score2 - expected_score2)

    # Round down the new ratings
    new_rating1 = math.floor(new_rating1)
    new_rating2 = math.floor(new_rating2)

    # Add logging
    print(f"New ELO: new_rating1={new_rating1}, new_rating2={new_rating2}")

    return new_rating1, new_rating2
