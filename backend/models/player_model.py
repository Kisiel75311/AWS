# backend/models/player_model.py
from models import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    elo_rating = db.Column(db.Integer)
    current_game_id = db.Column(db.Integer, nullable=True, unique=False)

    # # Zaktualizowana definicja relacji z Game
    # current_game = db.relationship('Game', foreign_keys=[current_game_id],
    #                                backref=db.backref('current_player_game', uselist=False), uselist=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.elo_rating = 1000

    def __repr__(self):
        return '<Player %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'elo_rating': self.elo_rating,
            'current_game_id': self.current_game_id
        }
