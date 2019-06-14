from player_ai import PlayerAI
from sensor import Sensor
from snakegame import Direction
import numpy as np


class PlayerAIGenetic(PlayerAI):

    def __init__(self, snake_list, food, box, network_list):

        super().__init__(snake_list[0], food, box)

        self.snake_list = snake_list
        self.network_list = network_list

        self.network = self.network_list[0]

        self.sensors = [Sensor(Direction.up, self.snake, self.box), Sensor(Direction.right, self.snake, self.box),
                        Sensor(Direction.down, self.snake, self.box), Sensor(Direction.left, self.snake, self.box)]

    def get_move(self):
        output = self.network.think(self.get_inputs())
        directions = [Direction.up, Direction.right, Direction.down, Direction.left]

        dir_index = directions.index(self.snake.direction)
        index = np.argmax(output)
        turn_index = index if index != 2 else -1

        result_index = dir_index + turn_index

        # because of array out of bounds
        result_index = 0 if result_index == 4 else result_index

        return directions[result_index]

    def get_inputs(self):
        sensors = self.get_sensors_inputs()
        food = self.get_food_inputs()
        # tail = self.get_tail_inputs()
        return np.concatenate((sensors, food))

    def get_sensors_inputs(self):
        current_direction_index = 0
        if self.snake.direction == Direction.right:
            current_direction_index = 1
        elif self.snake.direction == Direction.down:
            current_direction_index = 2
        elif self.snake.direction == Direction.left:
            current_direction_index = 3

        # Because of out of bounds array
        index_right = current_direction_index + 1
        index_right = 0 if index_right == 4 else index_right

        sensor_front = self.sensors[current_direction_index]
        sensor_right = self.sensors[index_right]
        sensor_left = self.sensors[current_direction_index - 1]

        sensor_front_out = self.__output_normalized__(sensor_front.distance_to_obstacle())
        sensor_right_out = self.__output_normalized__(sensor_right.distance_to_obstacle())
        sensor_left_out = self.__output_normalized__(sensor_left.distance_to_obstacle())

        return np.array([sensor_front_out, sensor_right_out, sensor_left_out])

    def get_food_inputs(self):
        return self.get_inputs_xy(self.food.position)

    # down: -x, y
    # left: -y, -x
    # up:   x, -y
    # right: y, x

    def get_inputs_xy(self, position):
        x = position[0]
        y = position[1]

        head_x = self.snake.head().position[0]
        head_y = self.snake.head().position[1]

        if not self.is_vertical_move():
            x, y = self.swap(x, y)
            head_x, head_y = self.swap(head_x, head_y)

        x_out = self.__output_normalized__(x - head_x)
        y_out = self.__output_normalized__(y - head_y)

        direction = self.snake.direction
        if direction == Direction.down or direction == Direction.left:
                x_out = -x_out
        if direction == Direction.up or direction == Direction.left:
                y_out = -y_out

        return np.array([x_out, y_out])

    @staticmethod
    def swap(x, y):
        return y, x

    def is_vertical_move(self):
        if self.snake.direction == Direction.up or self.snake.direction == Direction.down:
            return True
        return False

    # If the move is opposite to positive moves (up for y, right for x)
    def is_opposite_move(self):
        if self.snake.direction == Direction.down or self.snake.direction == Direction.left:
            return True
        return False

    def get_tail_inputs(self):
        return self.get_inputs_xy(self.snake.tail().position)

    def __output_normalized__(self, output):
        # For object right in front of snake, output must be one

        # if output < 0:
        #     normal_out = -(self.box.size() - (-output)) / self.box.size()
        # else:
        #     normal_out = (self.box.size() - (output - 1)) / self.box.size()
        normal_out = output/self.box.size()

        return normal_out

    def update(self, individual_index, food):
        self.snake = self.snake_list[individual_index]
        self.network = self.network_list[individual_index]
        self.update_food(food)

        for sensor in self.sensors:
            sensor.update_snake(self.snake)

    def reset(self):
        pass
