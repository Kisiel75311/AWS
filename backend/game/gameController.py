# backend/game/gameController.py
from .TicTacToe import TicTacToe
from models.game_model import Game
from models import db
from contextlib import contextmanager

from models.player_model import Player


class GameController:
    def __init__(self):
        self.games = {}

    def get_game(self, game_id):
        """ Pobierz grę z bazy danych lub stwórz nową instancję gry, jeśli nie istnieje. """
        game_record = db.session.get(Game, game_id)
            # db.session.get(Game, game_id)
        if game_record and game_id not in self.games:
            new_game = TicTacToe()
            new_game.set_board_state_from_string(game_record.board_state)
            new_game.current_player = game_record.current_player
            self.games[game_id] = new_game
        return self.games.get(game_id)

    def create_new_game(self, player_id):
        # Odłącz gracza od obecnej gry, jeśli jest już przypisany
        player = db.session.get(Player, player_id)
        if player.current_game_id:
            current_game = Game.query.get(player.current_game_id)
            if current_game.player1_id == player_id:
                current_game.player1_id = None
            elif current_game.player2_id == player_id:
                current_game.player2_id = None
            player.current_game_id = None
            db.session.commit()

        new_game = TicTacToe()
        game_record = Game(board_state=new_game.get_board_state(), current_player='X', winner=None, game_over=False,
                           player1_id=player_id)
        db.session.add(game_record)
        db.session.commit()
        new_game.id = game_record.id  # Przypisanie id do instancji gry
        self.games[game_record.id] = new_game
        player.current_game_id = game_record.id
        db.session.commit()
        return game_record.id, new_game.get_board_as_2d_array(), new_game.current_player


    def player_join_game(self, game_id, player_id):
        game = db.session.get(Game, game_id)
        player = db.session.get(Player, player_id)

        # Jeśli gracz jest już przypisany do innej gry, odłącz go
        if player.current_game_id and player.current_game_id != game_id:
            current_game = Game.query.get(player.current_game_id)
            if current_game.player1_id == player_id:
                current_game.player1_id = None
            elif current_game.player2_id == player_id:
                current_game.player2_id = None
            player.current_game_id = None
            db.session.commit()

        # Dodaj gracza do nowej gry
        if not game.player1_id:
            game.player1_id = player_id
        elif not game.player2_id and game.player1_id != player_id:
            game.player2_id = player_id
        else:
            raise Exception("Game already has two players or player is trying to join the same game.")

        player.current_game_id = game_id
        db.session.commit()

        return "Player joined the game", game.board_state, game.current_player


    def play_move(self, game_id, row, col, player_id):
        game_record = db.session.get(Game, game_id)
        if not game_record or game_record.game_over:
            return "Nie można grać w zakończoną grę.", None, None

        # Sprawdź, czy gracz jest jednym z graczy przypisanych do tej gry
        if player_id not in [game_record.player1_id, game_record.player2_id]:
            return "Gracz nie jest uczestnikiem tej gry.", None, None

        game = self.games.get(game_id)
        if not game:
            return "Gra nie została znaleziona.", None, None

        # Sprawdź, czy gracz ma prawo wykonać ruch
        if game.current_player != 'X' and game.current_player != 'O':
            return "Nieprawidłowa tura.", None, None

        if not game.make_move(row, col):
            return "Nieprawidłowy ruch.", None, None

        winner = game.check_winner()
        game_record.board_state = game.get_board_state()
        game_record.current_player = game.current_player

        game_over = False
        if winner:
            game_over = True
            game_record.game_over = True
            game_record.winner = winner
        elif game.is_full():
            game_over = True
            game_record.game_over = True
            game_record.winner = "Draw"

        db.session.commit()
        return ("Ruch wykonany pomyślnie.", game.get_board_as_2d_array(), game.current_player) if not game_over else \
            ("Gra zakończona: " + winner, game.get_board_as_2d_array(), game.current_player)


    def reset_game(self, game_id, player_id):
        game_record = db.session.get(Game, game_id)
        if not game_record:
            return "Gra nie została znaleziona.", None, None

        # Sprawdź, czy gracz jest jednym z graczy przypisanych do tej gry
        if player_id not in [game_record.player1_id, game_record.player2_id]:
            return "Gracz nie jest uczestnikiem tej gry.", None, None

        game = self.games.get(game_id)
        if not game:
            return "Gra nie została znaleziona.", None, None

        game.reset_board()
        game_record.board_state = game.get_board_state()
        game_record.current_player = game.current_player
        game_record.game_over = False
        game_record.winner = None

        db.session.commit()
        return "Gra została zresetowana.", game.get_board_as_2d_array(), 'X'
