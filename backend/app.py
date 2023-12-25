import sentry_sdk
from flask import Flask, jsonify
from flask_cors import CORS
from api.models import db

sentry_sdk.init(
    dsn="https://4cf6f815ee706c7a7e35b359fa634b7f@o4506447864463360.ingest.sentry.io/4506447866822656",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'  # Użyj bezpiecznego, stałego klucza
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Dodaj ten wiersz do konfiguracji
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
db.init_app(app)


def register_blueprints(app):
    from api.game_api import game_blueprint
    app.register_blueprint(game_blueprint, url_prefix='/api')


CORS(app)


@app.route('/api')
def index():
    return jsonify({"message": "Witaj w grze kółko i krzyżyk!"})


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Nie znaleziono strony."}), 404


if __name__ == '__main__':
    register_blueprints(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
