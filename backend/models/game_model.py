# backend/api/game_model.py
from models import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(255))
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    current_player = db.Column(db.String(1))
    current_player_id = db.Column(db.Integer)
    winner = db.Column(db.String(1))
    game_over = db.Column(db.Boolean)

    # Definicja relacji z player1 i player2

    def __init__(self, board_state, winner, game_over, current_player, player1_id=None, player2_id=None):
        self.board_state = board_state
        self.winner = winner
        self.game_over = game_over
        self.current_player = current_player
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.current_player_id = player1_id

    def __repr__(self):
        return '<Game %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'board_state': self.board_state,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'current_player': self.current_player,
            'winner': self.winner,
            'game_over': self.game_over
        }
