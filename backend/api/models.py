#backend/api/models.py

from flask_sqlalchemy import SQLAlchemy
from extensions import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String(9))  # Reprezentacja stanu planszy jako string
    current_player = db.Column(db.String(1))  # 'X' lub 'O'
    # Możesz dodać więcej pól, np. status gry, wynik itp.