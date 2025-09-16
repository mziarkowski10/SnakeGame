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
        self.players = [Snake([(32, 0), (16, 0), (0, 0)]), Snake([(352, 384), (368, 384), (384, 384)])]
        self.snakes = [s.curr_pos for s in self.players]
        self.food = Food().genereting_food(self.snakes)

    def calculate_state(self, client_update):
        self.tick += 1
        direction = client_update.get("direction")

        if client_update.get("player") >= len(self.players):
            # TODO Send error response
            return
    
        snake = self.players[client_update.get("player")]
        head = snake.move(direction)

        if head == self.food:
            self.food = Food().genereting_food(self.snakes)
        elif snake.last_move in OPPOSING_MOVE and direction != OPPOSING_MOVE[snake.last_move]:
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

    def genereting_food(self, snakes):
        while True:
            x = random.randrange(0, 400, 16)
            y = random.randrange(0, 400, 16)
            collision = False

            for s in snakes:
                if (x, y) in s:
                    collision = True
                    break

            if not collision:
                return x, y

class Snake:
    def __init__(self, pos):
        self.curr_pos = pos
        self.last_move = "ALL"

    def move(self, direction):
        if not self.curr_pos:
            return None
    
        if self.last_move in OPPOSING_MOVE and direction == OPPOSING_MOVE[self.last_move]:
            return self.curr_pos[0]
        
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