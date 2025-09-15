import pytest
from main import Food, Game, Snake, OPPOSING_MOVE

class TestMovement:

    #Four direction moving
    def test_move_to_the_right(self):
        snake = Snake([(0, 0)])
        head = snake.move("RIGHT")
        assert head == (16, 0)
        assert snake.last_move == "RIGHT"

    def test_move_to_the_left(self):
        snake = Snake([(384, 384)])
        head = snake.move("LEFT")
        assert head == (368, 384)
        assert snake.last_move == "LEFT"

    def test_move_to_the_up(self):
        snake = Snake([(384, 384)])
        head = snake.move("UP")
        assert head == (384, 368)
        assert snake.last_move == "UP"

    def test_move_to_the_down(self):
        snake = Snake([(0, 0)])
        head = snake.move("DOWN")
        assert head == (0, 16)
        assert snake.last_move == "DOWN"

    #Walking through the walls
    def test_through_the_wall_right(self):
        snake = Snake([(384, 384)])
        head = snake.move("RIGHT")
        assert head == (0, 384)
        assert snake.last_move == "RIGHT"

    def test_through_the_wall_left(self):
        snake = Snake([(0, 0)])
        head = snake.move("LEFT")
        assert head == (384, 0)
        assert snake.last_move == "LEFT"

    def test_through_the_wall_up(self):
        snake = Snake([(0, 0)])
        head = snake.move("UP")
        assert head == (0, 384)
        assert snake.last_move == "UP"

    def test_through_the_wall_down(self):
        snake = Snake([(384, 384)])
        head = snake.move("DOWN")
        assert head == (384, 0)
        assert snake.last_move == "DOWN"

class TestGame:

    #Eating apples
    def test_eating_apple(self):
        game = Game()
        snake = game.players[0]
        food = (48, 0)
        game.food = (48, 0)
        request = {
            "type": "move",
            "direction": "RIGHT",
            "player": 0
        }

        state = game.calculate_state(request)
        assert len(snake.curr_pos) == 4
        assert food != game.food

    #Game over
    def test_game_over(self):
        game = Game()
        snake = game.players[0]
        snake.curr_pos = ([(16, 16), (16, 32), (0, 32), (0, 16), (0, 0)])
        snake.move("LEFT")
        assert len(snake.curr_pos) != len(set(snake.curr_pos))

    #Turning back
    def test_turning_back(self):
        game = Game()
        snake = game.players[0]
        snake.last_move = "RIGHT"
        head_before = snake.curr_pos[0]
        head_after = snake.move("LEFT")

        assert head_before == head_after

    #Move one snake does not affect other
    def test_move_one_snake_does_not_affect_other(self):
        snake1 = Snake([(0, 0), (16, 0)])
        snake2 = Snake([(16, 0), (32, 0)])
        snake1.last_move = "RIGHT"
        head1 = snake1.curr_pos[0]
        head2 = snake2.move("LEFT")

        assert head1 == head2