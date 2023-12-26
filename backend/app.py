# backend/app.py
import sentry_sdk
from flask import Flask, jsonify
from flask_cors import CORS
from models.game_model import db

def create_app(testing=False):
    # Initialize Sentry SDK
    sentry_sdk.init(
        dsn="https://4cf6f815ee706c7a7e35b359fa634b7f@o4506447864463360.ingest.sentry.io/4506447866822656",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    # Create a Flask instance
    app = Flask(__name__)

    # Configure the app for testing or production
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF form validation, typically for testing
        app.secret_key = 'BAD_SECRET_KEY'  # Use a secure, constant key in production
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
        app.secret_key = 'BAD_SECRET_KEY'  # Use a secure, constant key in production
        app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize database
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Set up CORS
    CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})  # Możesz ograniczyć do konkretnych źródeł zamiast używać "*"

    # Define routes
    @app.route('/api')
    def index():
        return jsonify({"message": "Witaj w grze kółko i krzyżyk!"})

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"message": "Nie znaleziono strony."}), 404

    return app

def register_blueprints(app):
    from api.game_api import game_blueprint
    app.register_blueprint(game_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
