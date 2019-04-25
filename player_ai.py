from abstract_player import AbstractPlayer
from snake import Direction


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box):
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box

    def get_move(self):
        return Direction.none

    def reset(self):
        pass

