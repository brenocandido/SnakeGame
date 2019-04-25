from abstract_player import AbstractPlayer
from snake import Direction
from graph import Graph, Node


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box):
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box
        self.open_list = []
        self.closed_list = []
        self.obstacle_list = []
        self.move_list = []
        self.graph = Graph(Node(self.head_position(), 0))
        self.current_node = self.graph.root

    def get_move(self):
        return self.get_a_star_move()

    def get_a_star_move(self):
        self.obstacle_list = self.get_obstacle_list()
        self.get_move_list()
        return self.get_direction(self.head_position(), self.move_list[0].position)

    def get_move_list(self):  # TODO test if current F is the lowest of the graph

        while not self.objective_reached(self.current_node.position, self.objective_position()):

            self.current_node.add_open_list(self.get_open_list(self.current_node.position))
            closed_node = self.current_node.get_lowest_f()

            if not (closed_node is None):
                self.current_node.add_closed_node(closed_node)
                self.move_list.append(closed_node)
                self.current_node = closed_node

            else:  # No node returned
                self.return_to_previous_node()

    def get_open_list(self, position):
        neighbours = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        open_list = []

        for n in neighbours:
            sum = self.sum_tuple(position, n)
            if self.is_in_box(sum) and not (sum in self.obstacle_list):
                open_list.append(sum)

        return self.get_graph_open_list(open_list)

    def get_graph_open_list(self, open_list):
        graph_list = []
        for element_position in open_list:
            f = self.f(element_position, self.objective_position())
            graph_list.append(Node(element_position, f))

        return graph_list

    def return_to_previous_node(self):
        if len(self.move_list) == 0:
            pass

        else:
            if len(self.move_list - 1) == 0:
                self.current_node = self.graph.root

            else:
                self.current_node = self.move_list[len(self.move_list) - 1]

            del self.move_list[len(self.move_list)]

    def head_position(self):
        return self.snake.head().position

    def get_obstacle_list(self):
        obstacle_list = []
        for body in self.snake.body:
            if body != self.snake.head():
                obstacle_list.append(body.position)

        return obstacle_list

    @staticmethod
    def manhattan(start, end):
        return abs(end[0]-start[0]) + abs(end[1]-start[1])

    @staticmethod
    def sum_tuple( a, b):
        return a[0] + b[0], a[1] + b[1]

    def is_in_box(self, position):
        if 0 <= position[0] < self.box.size() and 0 <= position[1] < self.box.size():
            return True

        return False

    def objective_position(self):
        return self.food.position

    @staticmethod
    def objective_reached(position, objective_posisiton):
        return position == objective_posisiton

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
        self.open_list = []
        self.obstacle_list = []
        self.closed_list = []
        self.move_list = []
        self.graph = Graph(Node(self.head_position(), 0))
        self.current_node = self.graph.root
