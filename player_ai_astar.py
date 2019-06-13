from player_ai import PlayerAI
from a_star import AStar


class PlayerAIAStar(PlayerAI):

    def __init__(self, snake, food, score, box, wall_list):
        super().__init__(snake, food, score, box)

        self.obstacle_list = []
        self.a_star = AStar(box)
        self.wall_list = wall_list

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

    def get_obstacle_list(self):
        obstacle_list = []
        for body in self.snake.body:
            if body != self.snake.head():
                obstacle_list.append(body.position)

        for wall in self.wall_list:
            if wall not in obstacle_list:
                obstacle_list.append(wall)

        return obstacle_list

    def reset_lists(self):
        self.obstacle_list.clear()

