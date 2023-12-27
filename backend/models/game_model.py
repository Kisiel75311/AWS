# backend/api/game_model.py
from models import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(255))
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    winner = db.Column(db.String(1))
    game_over = db.Column(db.Boolean)

    # Definicja relacji z player1 i player2
    player1 = db.relationship('Player', foreign_keys=[player1_id], backref=db.backref('player1_games', lazy='dynamic'))
    player2 = db.relationship('Player', foreign_keys=[player2_id], backref=db.backref('player2_games', lazy='dynamic'))

    def __init__(self, board_state, winner, game_over):
        self.board_state = board_state
        self.winner = winner
        self.game_over = game_over

    def __repr__(self):
        return '<Game %r>' % self.id
