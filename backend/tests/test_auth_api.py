import pytest
from flask_testing import TestCase
from app import build_app, db
from flask import make_response
import json

from models.player_model import Player
import allure


@allure.feature('Authentication API')
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

    @allure.story('User registration')
    @allure.title('Registering a new user')
    def test_register_user(self):
        # Test registering a new user
        response = self.client.post('/auth/register', data=json.dumps({
            'username': '1newuser@example.com',
            'password': 'Newpassword1_'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Player registered successfully.", response.json['message'])

    @allure.story('User registration missing data')
    @allure.title('Registering a new user with missing data')
    def test_register_user_missing_data(self):
        # Test registration with missing username or password
        response = self.client.post('/auth/register', data=json.dumps({
            'password': 'newpassword'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username and password are required.", response.json['error'])

    @allure.story('User registration existing user')
    @allure.title('Registering an existing user')
    def test_register_existing_user(self):
        # Register a user
        self.test_register_user()

        # Try to register the same user again
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists.", response.json['error'])

    @allure.story('User login')
    @allure.title('Logging in a user')
    def test_login_user(self):
        # First, register a user
        self.test_register_user()
        # Then, try to login
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'newuser',
            'password': 'newpassword'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        self._login_response = response

    @allure.story('User login missing data')
    @allure.title('Logging in a user with missing data')
    def test_login_user_wrong_password(self):
        # First, register a user
        self.test_register_user()
        # Then, try to login with wrong password
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'newuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 401)

    @allure.story('User login nonexistent user')
    @allure.title('Logging in a nonexistent user')
    def test_login_nonexistent_user(self):
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'nonexistent',
            'password': 'password'
        }), content_type='application/json')
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 404)

    @allure.story('User logout')
    @allure.title('Logging out a user')
    def test_logout_user(self):
        # First, register and login a user to get a token
        response = self.test_login_user()
        token = json.loads(self._login_response.data)['token']
        # Then, try to logout
        response = self.client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        print('Response status code:', response.status_code)
        print('Response body:', response.json)
        self.assertEqual(response.status_code, 200)

    @allure.story('User logout missing token')
    @allure.title('Logging out a user without token')
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
            print('Response status code:', register_response.status_code)
            print('Response body:', register_response.json)

            # Login user
            login_response = self.client.post('/auth/login', data=json.dumps({
                'username': username,
                'password': password
            }), content_type='application/json')
            print('Response status code:', login_response.status_code)
            print('Response body:', login_response.json)

            self.assertEqual(login_response.status_code, 200)
            token = json.loads(login_response.data)['token']

            # Check if the token is already in the set
            self.assertNotIn(token, tokens)
            tokens.add(token)

        # Verify that 5 records exist in the Player table
        player_count = Player.query.count()
        self.assertEqual(player_count, num_users)
