import json
import os
from datetime import datetime, timedelta

import jwt
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from models.game_model import db
from models.player_model import Player


class AuthService:
    """Provides authentication-related functionality."""

    def __init__(self):
        """Initializes the AuthService instance."""
        self.invalidated_tokens_store = set()
        self.jwt_instance = jwt.JWT()

        # Load RSA keys
        self.signing_key = self.load_rsa_key(os.path.join(os.path.dirname(__file__), 'rsa_private_key.pem'))
        self.verifying_key = self.load_rsa_key(os.path.join(os.path.dirname(__file__), 'rsa_public_key.json'))

    def load_rsa_key(self, file_path):
        """Loads an RSA key from a file."""
        with open(file_path, 'r') as fh:
            key_dict = json.load(fh)
        return jwt.jwk_from_dict(key_dict)

    def generate_jwt_token(self, user_id: int) -> str:
        """Generates a JWT token for a user."""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),  # Token valid for 1 day
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return self.jwt_instance.encode(payload, self.signing_key, alg='RS256')
        except Exception as e:
            current_app.logger.exception(e)
            raise Exception("Failed to generate JWT token.")

    def decode_and_verify_token(self, token: str) -> dict:
        """Decodes and verifies a JWT token."""
        try:
            if token in self.invalidated_tokens_store:
                raise jwt.InvalidTokenError("Token has been invalidated.")

            payload = self.jwt_instance.decode(
                token, self.verifying_key, do_time_check=True)
            return payload

        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired.")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token.")
        except jwt.InvalidSignatureError:
            raise jwt.InvalidSignatureError("Invalid token signature.")
        except Exception as e:
            current_app.logger.exception(e)
            raise Exception("Failed to decode and verify JWT token.")

    def invalidate_token(self, token: str):
        self.invalidated_tokens_store.add(token)

    def is_token_invalidated(self, token: str) -> bool:
        return token in self.invalidated_tokens_store

    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)

    def check_password(self, hashed_password: str, password: str) -> bool:
        return check_password_hash(hashed_password, password)

    def register(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        new_player = Player(name=username)
        new_player.password = hashed_password
        db.session.add(new_player)
        db.session.commit()
        return "Player registered successfully."

    def login(self, username: str, password: str) -> str:
        player = Player.query.filter_by(name=username).first()
        if player and self.check_password(player.password, password):
            return self.generate_jwt_token(player.id)
        else:
            raise Exception("Invalid username or password.")

    def logout(self, token: str):
        self.invalidate_token(token)
        return "Player logged out successfully."
