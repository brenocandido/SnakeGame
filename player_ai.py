from abstract_player import AbstractPlayer
from snake import Direction
from graph import Graph, Node
from queue import PriorityQueue


class PlayerAI(AbstractPlayer):

    def __init__(self, snake, food, score, box, max_return_tries=300):
        self.priority_queue = PriorityQueue()
        self.snake = snake
        self.food = food
        self.score = score
        self.box = box
        self.open_list = []
        self.closed_list = []
        self.obstacle_list = []
        self.move_list = []
        self.full_move_list = []
        self.blocked_list = []          # List of nodes with dead ends
        self.came_from = {}
        self.graph = Graph(Node(self.head_position(), 0))
        self.current_node = self.graph.root
        self.return_tries = 0
        self.max_return_tries = max_return_tries

    def get_move(self):
        return self.get_a_star_move()

    def get_a_star_move(self):
        self.reset_lists()
        self.obstacle_list = self.get_obstacle_list()
        self.get_move_list()
        move = self.get_first_move()
        return self.get_direction(self.head_position(), move)

    def get_first_move(self):
        current = self.objective_position()
        start = self.head_position()
        move = start
        while current != start:
            try:
                move = current
                current = self.came_from[current]
            except:
                break

        return move

    def reset_lists(self):
        self.open_list = []
        self.closed_list = []
        self.obstacle_list = []
        self.move_list = []
        self.full_move_list = []
        self.priority_queue = PriorityQueue()
        self.blocked_list = []
        self.came_from = {}

    def get_move_list(self):
        count = 0
        start = self.head_position()
        goal = self.objective_position()
        self.priority_queue.put((0, start))
        self.came_from = {}
        cost_so_far = {}
        self.came_from[start] = None
        cost_so_far[start] = 0

        while not self.priority_queue.empty():
            current_position = self.priority_queue.get()[1]

            if self.objective_reached(current_position, goal):
                break

            for next_position in self.get_neighbors(current_position):
                cost = cost_so_far[current_position]
                new_cost = cost + 1 # Cost of moving a single position is 1

                if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                    cost_so_far[next_position] = new_cost
                    priority = new_cost + self.heuristic(next_position, goal)
                    self.priority_queue.put((priority, next_position))
                    self.came_from[next_position] = current_position

            count += 1

    def get_neighbors(self, position):
        neighbors = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        neighbors_list = []

        for n in neighbors:
            sum = self.sum_tuple(position, n)
            if self.is_in_box(sum) and not (sum in self.obstacle_list):
                neighbors_list.append(sum)

        return neighbors_list

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
            if len(self.move_list)-1 == 0:
                self.current_node = self.graph.root

            else:
                self.current_node = self.move_list[len(self.move_list) - 1]

            del self.move_list[len(self.move_list)-1]

    def head_position(self):
        return self.snake.head().position

    def get_obstacle_list(self):
        obstacle_list = []
        for body in self.snake.body:
            if body != self.snake.head():
                obstacle_list.append(body.position)

        return obstacle_list

    @staticmethod
    def heuristic(start, end):
        # Manhattan
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
        h = self.heuristic(start, end)

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
        self.reset_lists()
        self.graph = Graph(Node(self.head_position(), 0))
        self.current_node = self.graph.root
        self.return_tries = 0


class PriorityEntry(object):

    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __lt__(self, other):
        return self.priority > other.priority
