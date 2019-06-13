from sensor import Sensor
from a_star import AStar
from abstract_player import AbstractPlayer
from snake import Direction


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box):
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box

    def get_move(self):
        pass

    def head_position(self):
        return self.snake.head().position

    def is_in_box(self, position):
        if 0 <= position[0] < self.box.size() and 0 <= position[1] < self.box.size():
            return True

        return False

    def objective_position(self):
        return self.food.position

    @staticmethod
    def objective_reached(position, objective_positon):
        return position == objective_positon

    def update_food(self, food):
        self.food = food

    @staticmethod
    def get_direction(position, new_position):
        result = (new_position[0]-position[0], new_position[1]-position[1])
        direction = Direction.none
        if result == (1, 0):
            direction = Direction.right
        elif result == (-1, 0):
            direction = Direction.left
        elif result == (0, 1):
            direction = Direction.down
        elif result == (0, -1):
            direction = Direction.up

        return direction

    def reset(self):
        pass
