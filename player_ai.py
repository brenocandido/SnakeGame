from sensor import Sensor
from a_star import AStar
from abstract_player import AbstractPlayer
from snake import Direction


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box, wall_list):
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box
        self.wall_list = wall_list

        self.obstacle_list = []
        self.a_star = AStar(box)

    def get_move(self):
        return self.get_a_star_move()

    def get_a_star_move(self):
        self.obstacle_list = self.get_obstacle_list()

        move_list = self.a_star.get_a_star_move_list(self.head_position(),
                                                     self.objective_position(), self.obstacle_list)

        try:
            move = move_list[0]
        except:                 # No path to food possible
            move = self.survive()

        return self.get_direction(self.head_position(), move)

    def survive(self):
        neighbors = self.a_star.get_neighbors(self.head_position(), self.obstacle_list,
                                              direction_dependant=True, direction=self.snake.direction)
        move = self.head_position()

        if neighbors:       # If not empty
            move = neighbors[0]

        return move

    def reset_lists(self):
        self.obstacle_list.clear()

    def head_position(self):
        return self.snake.head().position

    def get_obstacle_list(self):
        obstacle_list = []
        for body in self.snake.body:
            if body != self.snake.head():
                obstacle_list.append(body.position)

        for wall in self.wall_list:
            if wall not in obstacle_list:
                obstacle_list.append(wall)

        return obstacle_list

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
        self.reset_lists()
