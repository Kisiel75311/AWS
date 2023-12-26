from flask import jsonify
from exceptions import InvalidPasswordException, UserNotFoundException, UserAlreadyExistsError
import logging

def register_error_handlers(app):
    @app.errorhandler(InvalidPasswordException)
    def handle_invalid_password_exception(error):
        logging.error(f"InvalidPasswordException: {error}")
        return jsonify({"message": error.message}), error.status_code

    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found_exception(error):
        logging.error(f"UserNotFoundException: {error}")
        return jsonify({"message": error.message}), error.status_code

    @app.errorhandler(UserAlreadyExistsError)
    def handle_user_already_exists_exception(error):
        logging.error(f"UserAlreadyExistsError: {error}")
        return jsonify({"message": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_exception(error):
        logging.error(f"Exception: {error}")
        return jsonify({"message": str(error)}), 500

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({"message": "Internal server error"}), 500
