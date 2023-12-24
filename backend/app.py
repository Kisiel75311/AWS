#backend/app.py
import sentry_sdk
from flask import Flask, jsonify
from api.game_api import game_blueprint  # Zakładając, że utworzyłeś Blueprint w game_api.py
from api.models import db

sentry_sdk.init(
    dsn="https://4cf6f815ee706c7a7e35b359fa634b7f@o4506447864463360.ingest.sentry.io/4506447866822656",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'  # Ścieżka do pliku bazy danych
db.init_app(app)

# Rejestrowanie Blueprint z game_api.py
app.register_blueprint(game_blueprint, url_prefix='/game')

@app.route('/')
def index():
    return jsonify({"message": "Witaj w grze kółko i krzyżyk!"})

if __name__ == '__main__':
    app.run(debug=True)

