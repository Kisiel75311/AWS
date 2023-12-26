# backedn/api_api.py
from flask import Blueprint, request, jsonify, current_app
from services.auth_service import AuthService
from exceptions import UserNotFoundException, InvalidPasswordException, UserAlreadyExistsError
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        message = auth_service.register(username, password)
        return jsonify({"message": message}), 201
    except UserAlreadyExistsError:
        return jsonify({"error": "User already exists."}), 409


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

    except InvalidPasswordException:
        return jsonify({"error": "Invalid password."}), 401
    except UserNotFoundException:
        return jsonify({"error": "User not found."}), 404


@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Flask-JWT-Extended does not support built-in logout or token invalidation.
    # You would need to implement a token denylist/revocation mechanism if needed.
    user_id = get_jwt_identity()
    # Here you can implement the logic to add the token to a denylist
    return jsonify({"message": f"User {user_id} logged out."}), 200
