from snake import Direction
from game_box import Item


class Sensor:

    def __init__(self, direction, snake, game_box, sensor_range=99999):
        self.direction = direction
        self.snake = snake
        self.game_box = game_box
        self.sensor_range = sensor_range

    def object_in_range(self):
        return self.get_object_position() == self.snake.head().position

    def distance_to_object(self):
        current_position = self.snake.head().position
        object_position = self.get_object_position()

        return abs(current_position[0] - object_position[0]) + abs(current_position[1] - object_position[1])

    def distance_to_obstacle(self):
        current_position = self.snake.head().position
        obstacle_position = self.get_obstacle_position()

        return abs(current_position[0] - obstacle_position[0]) + abs(current_position[1] - obstacle_position[1])

    def get_object_position(self):
        current_position = self.snake.head().position

        for i in range(self.sensor_range):
            distance = i + 1
            next_position = self.get_next_position(current_position, distance)

            if self.game_box.is_in_box(next_position):
                if self.game_box.is_occupied(next_position):
                    return next_position

            else:
                return next_position

        return current_position

    def distance_to_item(self, item):
        current_position = self.snake.head().position
        item_position = self.get_item_position(item)

        if not self.game_box.is_in_box(item_position):
            return self.game_box.size()
        else:
            return abs(current_position[0] - item_position[0]) + abs(current_position[1] - item_position[1])

    def get_item_position(self, item):
        current_position = self.snake.head().position

        for i in range(self.sensor_range):
            distance = i + 1
            next_position = self.get_next_position(current_position, distance)

            if self.game_box.is_in_box(next_position):
                if self.game_box.item(next_position) == item:
                    return next_position

            else:
                return next_position

        return current_position

    def get_obstacle_position(self):
        current_position = self.snake.head().position

        for i in range(self.sensor_range):
            distance = i + 1
            next_position = self.get_next_position(current_position, distance)

            if self.game_box.is_in_box(next_position):
                if self.game_box.is_occupied(next_position) and self.game_box.item(next_position) != Item.food:
                    return next_position

            else:
                return next_position

        return current_position

    def get_food_position(self):
        position = self.get_item_position(Item.food)
        return position

    def get_object_type(self):
        object_position = self.get_object_position()

        if self.game_box.is_in_box(object_position):
            return self.game_box.item(object_position)

        else:
            return Item.wall

    def get_next_position(self, current_position, distance):

        direction = self.direction
        secondary_direction = self.get_secondary_direction(direction)      # for diagonal

        if self.is_diagonal_up(direction):
            direction = Direction.up
        elif self.is_diagonal_down(direction):
            direction = Direction.down

        if direction == Direction.up:
            return current_position[0], current_position[1] - distance

        elif direction == Direction.down:
            return current_position[0], current_position[1] + distance

        elif direction == Direction.left:
            return current_position[0] - distance, current_position[1]

        elif direction == Direction.right:
            return current_position[0] + distance, current_position[1]

        if secondary_direction is not None:
            self.get_next_position(secondary_direction, distance)

    # For diagonal sensors
    def get_secondary_direction(self, direction):
        if not self.is_diagonal_direction(direction):
            return None

        if direction == Direction.down_left or Direction.up_left:
            return Direction.left

        else:
            return Direction.right

    def is_diagonal_direction(self, direction):
        return self.is_diagonal_up(direction) or self.is_diagonal_down(direction)

    @staticmethod
    def is_diagonal_up(direction):
        return direction == Direction.up_right or direction == Direction.up_left

    @staticmethod
    def is_diagonal_down(direction):
        return direction == Direction.down_right or direction == Direction.down_left

    def update_snake(self, snake):
        self.snake = snake
