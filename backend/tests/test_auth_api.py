import pytest
from flask_testing import TestCase
from app import create_app, db
import json


class TestAuthAPI(TestCase):
    def create_app(self):
        # Konfiguracja aplikacji dla testów
        app = create_app(testing=True)
        return app

    def setUp(self):
        # Ustawienie bazy danych przed każdym testem
        db.create_all()

    def tearDown(self):
        # Czyszczenie bazy danych po każdym teście
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        # Testowanie rejestracji użytkownika
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        # Testowanie logowania użytkownika
        self.test_register_user()  # Najpierw zarejestruj użytkownika
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_logout_user(self):
        # Testowanie wylogowania użytkownika
        self.test_login_user()  # Najpierw zaloguj użytkownika
        token = json.loads(response.data)['token']
        response = self.client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_user_missing_data(self):
        # Test rejestracji z brakującymi danymi
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'testuser'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_existing_user(self):
        # Test rejestracji istniejącego użytkownika
        self.test_register_user()  # Najpierw zarejestruj użytkownika
        response = self.client.post('/auth/register', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_user_wrong_password(self):
        # Test logowania z nieprawidłowym hasłem
        self.test_register_user()  # Najpierw zarejestruj użytkownika
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'testuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_nonexistent_user(self):
        # Test logowania nieistniejącego użytkownika
        response = self.client.post('/auth/login', data=json.dumps({
            'username': 'nonexistent',
            'password': 'password'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_logout_with_invalid_token(self):
        # Test wylogowywania z niepoprawnym tokenem
        response = self.client.post('/auth/logout', headers={
            'Authorization': 'Bearer invalidtoken'
        })
        self.assertEqual(response.status_code, 400)

    def test_logout_without_token(self):
        # Test wylogowywania bez tokena
        response = self.client.post('/auth/logout')
        self.assertEqual(response.status_code, 400)
