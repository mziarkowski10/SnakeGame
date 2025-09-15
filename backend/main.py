import json
import random
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
from copy import deepcopy


app = Flask(__name__)
CORS(app)

OPPOSING_MOVE = {
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "UP": "DOWN",
    "RIGHT": "LEFT",
    "ALL": "ALL"
}

class Game:
    def __init__(self):
        self.tick = 0
        self.players = [Snake([(0, 0), (0, 16), (16, 0)]), Snake([(384, 384), (368, 384), (384, 368)])]
        self.food = Food().genereting_food()

    def calculate_state(self, client_update):
        self.tick += 1
        direction = client_update.get("direction")

        if client_update.get("player") >= len(self.players):
            # TODO Send error response
            return
    
        snake = self.players[client_update.get("player")]
        head = snake.move(direction)

        if head == self.food:
            self.food = Food().genereting_food()
        else:
            snake.curr_pos.pop()

        if snake.is_game_over():
            return {
                "type": "gameover"
            }

        response =  {
            "type": "state",
            "food": self.food
        }

        response["players"] = []

        for id, player in enumerate(self.players):
            response["players"].append({
                "player": id,
                "snake": player.curr_pos,
            })

        return response


class Food:
    def __init__(self):
        pass

    def genereting_food(self):
        x = random.randrange(0, 400, 16)
        y = random.randrange(0, 400, 16)

        return x, y

class Snake:
    def __init__(self, pos):
        self.curr_pos = pos
        self.last_move = "ALL"

    def move(self, direction):
        if direction == OPPOSING_MOVE[self.last_move]:
            return head

        head = list(self.curr_pos[0])

        if direction == "UP":
            head[1] -= 16
        elif direction == "DOWN":
            head[1] += 16
        elif direction == "LEFT":
            head[0] -= 16
        elif direction == "RIGHT":
            head[0] += 16
        else:
            return head
            
        if head[0] < 0:
            head[0] = 384
        if head[0] >= 400:
            head[0] = 0
        if head[1] < 0:
            head[1] = 384
        if head[1] >= 400:
            head[1] = 0

        head = tuple(head)
        self.curr_pos.insert(0, head)

        self.last_move = direction

        return head
    
    def is_game_over(self):
        return len(self.curr_pos) != len(set(self.curr_pos))

game = Game()

if __name__ == "__main__":
    pass 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/move', methods=['POST']) 
def foo():
    print(request.json)
    return jsonify(game.calculate_state(request.json))

#Poruszanie sie w 4 kierunkach
#Przechodzenie przez sciany
#Zjadanie jablka i rosniecie
#Porusznie wasd
#Kolizja wewnetrzna
#Nie można wejsc w siebie
#Testy
#Ruch jednego weza nie moze cofać drugiego