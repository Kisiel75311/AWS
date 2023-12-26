# backend/models/player_model.py
from models.game_model import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(128), nullable=False)
    games = db.relationship('Game', backref='player', lazy=True)
    elo_rating = db.Column(db.Integer)
    curren_game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.elo_rating = 1000

    def __repr__(self):
        return '<Player %r>' % self.name