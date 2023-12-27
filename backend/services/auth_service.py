# backend/services/auth_service.py
from sqlite3 import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.game_model import db
from models.player_model import Player

from exceptions import UserAlreadyExistsError

from exceptions import InvalidPasswordException, UserNotFoundException


class AuthService:
    """Provides authentication-related functionality."""

    def __init__(self):
        """Initializes the AuthService instance."""
        self.invalidated_tokens_store = set()

    def generate_jwt_token(self, user_id: int) -> str:
        """Generates a JWT token for a user."""
        try:
            # No need for additional claims if you only want to store user_id in token
            return create_access_token(identity=user_id)
        except Exception as e:
            raise Exception("Failed to generate JWT token.")

    # Remove decode_and_verify_token as it's managed internally by Flask-JWT-Extended

    def invalidate_token(self, token: str):
        """Invalidates a JWT token."""
        # Token invalidation logic (if you're implementing token denylisting)
        self.invalidated_tokens_store.add(token)

    def is_token_invalidated(self, token: str) -> bool:
        """Checks if a token is invalidated."""
        return token in self.invalidated_tokens_store

    def hash_password(self, password: str) -> str:
        """Hashes a password."""
        return generate_password_hash(password)

    def check_password(self, hashed_password: str, password: str) -> bool:
        """Checks a password against the hashed version."""
        return check_password_hash(hashed_password, password)

    def register(self, username: str, password: str):
        """Registers a new user."""
        # Check if the user already exists in the database
        existing_user = Player.query.filter_by(name=username).first()
        if existing_user:
            raise UserAlreadyExistsError("User already exists.")

        try:
            hashed_password = self.hash_password(password)
            new_player = Player(name=username, password=hashed_password)
            db.session.add(new_player)
            db.session.commit()
            return "Player registered successfully."
        except IntegrityError as e:
            db.session.rollback()
            raise  # Re-raise the original exception

    def login(self, username: str, password: str) -> str:
        """Logs in a user."""
        player = Player.query.filter_by(name=username).first()

        # Check if user exists
        if player is None:
            raise UserNotFoundException("Invalid username or password.")

        # Check if the password is correct
        if self.check_password(player.password, password):
            return self.generate_jwt_token(player.id)
        else:
            raise InvalidPasswordException("Invalid username or password.")
    def logout(self, token: str):
        """Logs out a user."""
        self.invalidate_token(token)
        return "Player logged out successfully."

    def get_player_id(self, username: str) -> int:
        """Retrieves the player's ID based on the username."""
        player = Player.query.filter_by(name=username).first()
        if player:
            return player.id
        else:
            raise UserNotFoundException("User not found.")