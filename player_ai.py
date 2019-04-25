from abstract_player import AbstractPlayer
from snake import Direction


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box):
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box
        self.open_list = []
        self.obstacle_list = []

    def get_move(self):
        return self.get_a_star_move()

    def reset(self):
        self.open_list = []
        self.obstacle_list = []

    def head_position(self):
        return self.snake.head().position

    def get_obstacle_list(self):
        obstacle_list = []
        for body in self.snake.body:
            if body != self.snake.head():
                obstacle_list.append(body.position)

        return obstacle_list

    def manhattan(self, start, end):
        return abs(end[0]-start[0]) + abs(end[1]-start[1])

    def sum_tuple(self, a, b):
        return (a[0] + b[0], a[1] + b[1])

    def is_in_box(self, position):
        if 0 <= position[0] < self.box.size() and 0 <= position[1] < self.box.size():
            return True

        return False

    def objective_position(self):
        return self.food.position

    def get_a_star_move(self):
        self.obstacle_list = self.get_obstacle_list()
        self.open_list = self.get_open_list()
        return self.get_best_move()

    def get_open_list(self):
        neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        open_list = []

        for n in neighbours:
            sum = self.sum_tuple(self.head_position(), n)
            if self.is_in_box(sum) and not sum in self.obstacle_list:
                open_list.append(sum)

        return open_list

    def update_food(self, food):
        self.food = food

    def f(self, start, end):
        g = 1
        h = self.manhattan(start, end)

        return g + h

    def get_best_move(self):
        f = 1000000
        new_position = self.head_position()
        for m in self.open_list:
            new_f = self.f(m, self.objective_position())
            if new_f <= f:
                f = new_f
                new_position = m

        return self.get_direction(self.head_position(), new_position)

    def get_direction(self, position, new_position):
        result = (new_position[0]-position[0], new_position[1]-position[1])
        direction = Direction.none
        if result == (1,0):
            direction = Direction.right
        elif result == (-1,0):
            direction = Direction.left
        elif result == (0,1):
            direction = Direction.down
        elif result == (0, -1):
            direction = Direction.up

        return direction
