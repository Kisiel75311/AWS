# backend/api/game_model.py
from models import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(255))
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id', use_alter=True, name='fk_player1_id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id', use_alter=True, name='fk_player2_id'))
    current_player = db.Column(db.String(1))
    winner = db.Column(db.String(1))
    game_over = db.Column(db.Boolean)

    # Definicja relacji z player1 i player2
    player1 = db.relationship('Player', foreign_keys=[player1_id], backref=db.backref('player1_games', lazy='dynamic'))
    player2 = db.relationship('Player', foreign_keys=[player2_id], backref=db.backref('player2_games', lazy='dynamic'))

    def __init__(self, board_state, winner, game_over, current_player, player1_id=None, player2_id=None):
        self.board_state = board_state
        self.winner = winner
        self.game_over = game_over
        self.current_player = current_player
        self.player1_id = player1_id
        self.player2_id = player2_id

    def __repr__(self):
        return '<Game %r>' % self.id
