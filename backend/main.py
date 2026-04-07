from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.game import Game


app = Flask(__name__)
CORS(app)

game = Game()
highscore = 0

@app.route('/move', methods=['POST']) 
def move():
    global highscore
    state = game.calculate_state(request.json)

    if state.get("type") == "gameover":
        score = state.get("points", 0)

        if score > highscore:
            highscore = score
            state["new_highscore"] = True
        else:
            state["new_highscore"] = False

    return jsonify(state)

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = Game()
    return {
        "status": "ok"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)