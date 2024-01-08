import boto3
import hmac
import hashlib
import base64
from flask import current_app
import logging

from exceptions import InvalidPasswordException, UserNotFoundException


class CognitoService:
    def __init__(self, aws_region, client_id, client_secret):
        self.client = boto3.client('cognito-idp', region_name=aws_region)
        self.client_id = client_id
        self.client_secret = client_secret

    def calculate_secret_hash(self, username):
        message = username + current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID']
        dig = hmac.new(
            str(current_app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET']).encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def sign_up_user(self, username, password):
        logging.info(f"udalo sie wywolac funckje sign_up_user")
        if not password:
            raise ValueError("Password cannot be empty")

        try:
            secret_hash = self.calculate_secret_hash(username)
            self.client.sign_up(
                ClientId=self.client_id,
                SecretHash=secret_hash,
                Username=username,
                Password=password
            )
            logging.info(f"User {username} signed up successfully.")
            return True
        except self.client.exceptions.UsernameExistsException as e:
            logging.error(f"User {username} already exists: {e}")
            return False

    def authenticate_user(self, username, password):
        try:
            secret_hash = self.calculate_secret_hash(username)
            response = self.client.initiate_auth(
                ClientId=current_app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'],
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash
                }
            )
            return response['AuthenticationResult']['IdToken']
        except self.client.exceptions.NotAuthorizedException:
            raise InvalidPasswordException("Invalid username or password.")
        except self.client.exceptions.UserNotFoundException:
            raise UserNotFoundException("User not found.")
