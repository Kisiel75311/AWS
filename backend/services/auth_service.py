import boto3
from flask import current_app
from psycopg2 import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from models.player_model import Player
from exceptions import UserAlreadyExistsError, InvalidPasswordException, UserNotFoundException
from models import db
import hmac, hashlib, base64


class AuthService:
    """Provides authentication-related functionality."""

    def __init__(self):
        """Initializes the AuthService instance."""
        self.cognito_client = boto3.client('cognito-idp')

    def cognito_generate_jwt_token(self, username: str, password: str) -> str:
        """Uses AWS Cognito to authenticate the user and get JWT token."""
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'],
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            return response['AuthenticationResult']['IdToken']
        except self.cognito_client.exceptions.NotAuthorizedException:
            raise InvalidPasswordException("Invalid username or password.")
        except self.cognito_client.exceptions.UserNotFoundException:
            raise UserNotFoundException("User not found.")
        except Exception as e:
            raise Exception(f"Failed to authenticate with Cognito: {str(e)}")

    def register(self, username: str, password: str):
        """Registers a new user in the local database and Cognito."""
        # Check if the user already exists in the local database
        existing_user = Player.query.filter_by(name=username).first()
        if existing_user:
            raise UserAlreadyExistsError("User already exists in local database.")

        # Register user in Cognito
        try:
            secret_hash = calculate_secret_hash(username,
                                                current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'],
                                                current_app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'])

            self.cognito_client.sign_up(
                ClientId=current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'],
                SecretHash=secret_hash,  # Poprawiona nazwa parametru
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': username  # Assuming username is the email
                    },
                ]
            )
        except self.cognito_client.exceptions.UsernameExistsException as e:
            raise UserAlreadyExistsError("User already exists in Cognito.")

        # Add user to local database
        try:
            hashed_password = generate_password_hash(password)  # Generuj hash hasła
            new_player = Player(name=username, password=hashed_password)
            db.session.add(new_player)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise  # re-raise the exception

        return "Player registered successfully."

    def login(self, username: str, password: str) -> str:
        """Logs in a user using Cognito."""
        return self.cognito_generate_jwt_token(username, password)

    def logout(self, token: str):
        """Logs out a user."""
        return "Player logged out successfully."

    def get_player_id(self, username: str) -> int:
        """Retrieves the player's ID based on the username."""
        player = Player.query.filter_by(name=username).first()
        if player:
            return player.id
        else:
            raise UserNotFoundException("User not found.")


def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=message.encode('utf-8'),
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()
