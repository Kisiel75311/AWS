# backend/api/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(255))
    current_player = db.Column(db.String(1))
    winner = db.Column(db.String(1))
    game_over = db.Column(db.Boolean)

    def __init__(self, board_state, current_player, winner, game_over):
        self.board_state = board_state
        self.current_player = current_player
        self.winner = winner
        self.game_over = game_over

    def __repr__(self):
        return '<Game %r>' % self.id
