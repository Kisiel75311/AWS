# backend/services/auth_service.py
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from flask import current_app, jsonify
from models.player_model import Player
from exceptions.exceptions import UserNotFoundException, InvalidPasswordException

class AuthService:
    def register_user(self, username, password):
        if Player.query.filter_by(name=username).first():
            raise UserNotFoundException(f"User with username '{username}' already exists.")

        hashed_password = generate_password_hash(password)
        new_player = Player(name=username, password=hashed_password, elo_rating=1000)
        current_app.db.session.add(new_player)
        current_app.db.session.commit()

        return jsonify({"message": f"User '{username}' registered successfully."})

    def authenticate_user(self, username, password):
        player = Player.query.filter_by(name=username).first()

        if not player or not check_password_hash(player.password, password):
            raise InvalidPasswordException("Invalid username or password.")

        return player

    def logout_user(self, username):
        # Implement a logout mechanism if needed, e.g., invalidating the user's token
        pass

    def generate_jwt_token(self, user_id):
        # Implement a JWT token generation mechanism if needed
        pass

    def __repr__(self):
        return '<AuthService>'
