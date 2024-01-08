import boto3
from flask import current_app
from psycopg2 import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from models.player_model import Player
from exceptions import UserAlreadyExistsError, InvalidPasswordException, UserNotFoundException
from models import db
from flask_jwt_extended import create_access_token
import hmac, hashlib, base64
import logging
from services.CognitoService import CognitoService


class AuthService:
    def __init__(self, cognito_service):
        self.cognito_service = cognito_service

    def register(self, username, password):
        logging.info(f"Registering user: {username}, password: {password}")
        if not password:
            raise ValueError("Password cannot be empty")

        if self.cognito_service.sign_up_user(username, password):
            try:
                hashed_password = generate_password_hash(password)
                new_player = Player(name=username, password=hashed_password)
                db.session.add(new_player)
                db.session.commit()
                logging.info(f"User {username} registered successfully.")
                return True
            except IntegrityError as e:
                db.session.rollback()
                logging.error(f"Error registering user {username}: {e}")
                raise
        else:
            logging.error(f"User {username} already exists.")
            raise UserAlreadyExistsError("User already exists.")

    def login(self, username, password):
        # generate jwt token
        player_id = self.get_player_id(username)
        token = self.generate_jwt_token(player_id)

        return self.cognito_service.authenticate_user(username, password), token

    def get_player_id(self, username):
        player = Player.query.filter_by(name=username).first()
        if player:
            return player.id
        else:
            raise UserNotFoundException("User not found.")

    def generate_jwt_token(self, user_id: int) -> str:
        try:
            # No need for additional claims if you only want to store user_id in token
            return create_access_token(identity=user_id)
        except Exception as e:
            raise Exception("Failed to generate JWT token.")

