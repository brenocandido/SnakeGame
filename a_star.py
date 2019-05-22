
from queue import PriorityQueue
from snake import Direction

class A_Star:

    def __init__(self, box):
        self.priority_queue = PriorityQueue()
        self.came_from = {}
        self.game_box = box

    def get_a_star_move_list(self, start, goal, obstacle_list):

        self.reset_lists()
        self.calculate_a_star(start, goal, obstacle_list)
        return self.get_move_list(start, goal)

    def get_move_list(self, start, goal):
        current = goal
        move_list = []
        while current != start:
            try:
                move_list.insert(0, current)
                current = self.came_from[current]
            except:     # No path to food possible
                move_list = []
                break

        return move_list

    def calculate_a_star(self, start, goal, obstacle_list):
        self.priority_queue.put((0, start))
        self.came_from = {}
        cost_so_far = {start: 0}
        self.came_from[start] = None

        while not self.priority_queue.empty():
            current_position = self.priority_queue.get()[1]

            if self.objective_reached(current_position, goal):
                break

            for next_position in self.get_neighbors(current_position, obstacle_list):
                cost = cost_so_far[current_position]
                new_cost = cost + 1     # Cost of moving a single position is 1

                if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                    cost_so_far[next_position] = new_cost
                    priority = new_cost + self.heuristic(next_position, goal)
                    self.priority_queue.put((priority, next_position))
                    self.came_from[next_position] = current_position

    def get_neighbors(self, position, obstacle_list, direction_dependant=False, direction=Direction.up):
        neighbors = [(1, 0), (0, -1), (-1, 0), (0, 1)]

        if direction_dependant:     # Case up included in the initial values
            if direction == Direction.right:
                neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            elif direction == Direction.down:
                neighbors = [(0, 1), (1, 0), (-1, 0), (0, -1)]

            elif direction == Direction.left:
                neighbors = [(0, 1), (-1, 0), (0, -1), (1, 0)]

        neighbors_list = []

        for n in neighbors:
            sum = self.sum_tuple(position, n)
            if self.game_box.is_in_box(sum) and not (sum in obstacle_list):
                neighbors_list.append(sum)

        return neighbors_list

    @staticmethod
    def sum_tuple( a, b):
        return a[0] + b[0], a[1] + b[1]

    @staticmethod
    def heuristic(start, end):
        # Manhattan
        return abs(end[0]-start[0]) + abs(end[1]-start[1])

    @staticmethod
    def objective_reached(position, objective_positon):
        return position == objective_positon

    def reset_lists(self):
        self.priority_queue = PriorityQueue()
        self.came_from.clear()