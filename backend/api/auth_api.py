# backend/api/auth_api.py
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from exceptions import UserNotFoundException, InvalidPasswordException
auth_blueprint = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        auth_service.register(username, password)
        return jsonify({"message": f"User '{username}' registered successfully."}), 201

    except UserNotFoundException as e:
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        token = auth_service.login(username, password)
        return jsonify({"token": token}), 200

    except InvalidPasswordException as e:
        return jsonify({"error": str(e)}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization').split(' ')[1]

    if not token:
        return jsonify({"error": "Authorization header is missing or invalid."}), 400

    try:
        auth_service.invalidate_token(token)
        return jsonify({"message": "User logged out."}), 200

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({"error": "Failed to log out user."}), 500
