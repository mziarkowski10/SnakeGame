from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game


app = Flask(__name__)
CORS(app)

game = Game()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/move', methods=['POST']) 
def move():
    return jsonify(game.calculate_state(request.json))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)