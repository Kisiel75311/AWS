import pytest
from flask_testing import TestCase
from app import build_app, db
from flask import make_response
import json

from models.player_model import Player


class TestAuthAPI(TestCase):
    def create_app(self):
        # Konfiguracja aplikacji dla testów
        app = build_app(testing=True)
        return app

    def setUp(self):
        # Ustawienie bazy danych przed każdym testem
        db.create_all()

    def tearDown(self):
        # Czyszczenie bazy danych po każdym teście
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        # Test registering a new user
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Player registered successfully.", response.json['message'])

    def test_register_user_missing_data(self):
        # Test registration with missing username or password
        response = self.client.post('/auth/register', data=json.dumps({
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username and password are required.", response.json['error'])

    def test_register_existing_user(self):
        # Register a user
        self.test_register_user()

        # Try to register the same user again
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists.", response.json['error'])

    def test_login_user(self):
        # First, register a user
        self.test_register_user()
        # Then, try to login
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        return response

    def test_login_user_wrong_password(self):
        # First, register a user
        self.test_register_user()
        # Then, try to login with wrong password
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'newuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_nonexistent_user(self):
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'nonexistent',
            'password': 'password'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_logout_user(self):
        # First, register and login a user to get a token
        response = self.test_login_user()
        token = json.loads(response.data)['token']
        # Then, try to logout
        response = self.client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)

    def test_multiple_user_registration_and_login(self):
        # Number of users to test
        num_users = 5

        # Store the tokens to verify uniqueness
        tokens = set()

        for i in range(num_users):
            username = f'user{i}'
            password = f'pass{i}'

            # Register user
            register_response = self.client.post('/auth/register', data=json.dumps({
                'username': username,
                'password': password
            }), content_type='application/json')
            self.assertEqual(register_response.status_code, 201)

            # Login user
            login_response = self.client.post('/auth/login', data=json.dumps({
                'username': username,
                'password': password
            }), content_type='application/json')

            self.assertEqual(login_response.status_code, 200)
            token = json.loads(login_response.data)['token']

            # Check if the token is already in the set
            self.assertNotIn(token, tokens)
            tokens.add(token)

        # Verify that 5 records exist in the Player table
        player_count = Player.query.count()
        self.assertEqual(player_count, num_users)

