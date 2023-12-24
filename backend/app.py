from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Witaj w grze kółko i krzyżyk!"})

if __name__ == '__main__':
    app.run(debug=True)
