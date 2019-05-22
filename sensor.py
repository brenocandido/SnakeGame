from snake import Direction
from game_box import Item


class Sensor:

    def __init__(self, sensor_range, direction, snake, game_box):
        self.sensor_range = sensor_range
        self.direction = direction
        self.snake = snake
        self.game_box = game_box

    def object_in_range(self):
        return self.get_object_position() == self.snake.head().position

    def distance_to_object(self):
        current_position = self.snake.head().position
        object_position = self.get_object_position()

        return abs(current_position[0] - object_position[0]) + abs(current_position[1] - object_position[1])

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

    def get_object_type(self):
        object_position = self.get_object_position()

        if self.game_box.is_in_box(object_position):
            return self.game_box.item(object_position)

        else:
            return Item.wall

    def get_next_position(self, current_position, distance):

        if self.direction == Direction.up:
            return current_position[0], current_position[1] - distance

        elif self.direction == Direction.down:
            return current_position[0], current_position[1] + distance

        elif self.direction == Direction.left:
            return current_position[0] - distance, current_position[1]

        elif self.direction == Direction.right:
            return current_position[0] + distance, current_position[1]

        raise Exception("Sensor direction not specified")
        return current_position
