# backend/app.py
import sentry_sdk
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from error_hanlers import register_error_handlers

def build_app(testing=False):
    # Initialize Sentry SDK
    sentry_sdk.init(
        dsn="https://4cf6f815ee706c7a7e35b359fa634b7f@o4506447864463360.ingest.sentry.io/4506447866822656",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

    # Create a Flask instance
    app = Flask(__name__)
    app.config.from_object(Config)

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

    migrate = Migrate(app, db)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # Set up CORS
    CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})  # Możesz ograniczyć do konkretnych źródeł zamiast używać "*"
    jwt = JWTManager(app)

    # Register error handlers
    register_error_handlers(app)

    # Define routes
    @app.route('/api')
    def index():
        return jsonify({"message": "Witaj w grze kółko i krzyżyk!"})

    # Swagger configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Game API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

def register_blueprints(app):
    from api.game_api import game_blueprint
    from api.auth_api import auth_blueprint

    app.register_blueprint(game_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app = build_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
