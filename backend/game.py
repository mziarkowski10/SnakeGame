import random


OPPOSING_MOVE = {
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "UP": "DOWN",
    "RIGHT": "LEFT"
}


class Game:
    def __init__(self):
        self.tick = 0
        self.player = Snake([(32, 0), (16, 0), (0, 0)])
        self.snake = self.player.curr_pos
        self.food = Food().generate_food(self.snake)
        self.game_over = False

    def calculate_state(self, client_update):
        if self.game_over:
            return {
                "type": "gameover"
            }

        self.tick += 1
        direction = client_update.get("direction")

        if client_update.get("player") is None or client_update.get("player") != 0:
            return {
                "type": "error",
                "message": "Invalid player (only player 0 is allowed)"
            }
    
        snake = self.player
        head = snake.move(direction)

        if head == self.food:
            self.food = Food().generate_food(self.snake)
        else:
            snake.curr_pos.pop()

        if snake.is_game_over():
            self.game_over = True
            return {
                "type": "gameover"
            }

        response =  {
            "type": "state",
            "food": self.food,
            "player": {
                "id": 0,
                "position": snake.curr_pos
            }
        }

        return response


class Food:
    def __init__(self):
        pass

    def generate_food(self, snake):
        while True:
            x = random.randrange(0, 400, 16)
            y = random.randrange(0, 400, 16)
            collision = False

            if (x, y) in snake:
                collision = True

            if not collision:
                return x, y

class Snake:
    def __init__(self, pos):
        self.curr_pos = pos
        self.last_move = None

    def move(self, direction):
        if not self.curr_pos:
            return None
    
        if self.last_move and direction == OPPOSING_MOVE[self.last_move]:
            direction = self.last_move
        
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