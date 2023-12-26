# backend/api/auth_api.py
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    # Logika endpointu rejestracji
    pass

@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Logika endpointu logowania
    pass

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # Logika endpointu wylogowania
    pass