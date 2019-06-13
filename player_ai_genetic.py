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
        turn_index = 0

        if np.array_equal(output, [0, 1, 0]):   # Right
            turn_index = 1

        elif np.array_equal(output, [0, 0, 1]):   # Left
            turn_index = -1

        return directions[dir_index + turn_index]

    def get_inputs(self):
        sensors = self.get_sensors_inputs()
        food = self.get_food_inputs()
        tail = self.get_tail_inputs()
        return np.concatenate((sensors, food, tail))

    def get_sensors_inputs(self):
        current_direction_index = 0
        if self.snake.direction == Direction.right:
            current_direction_index = 1
        elif self.snake.direction == Direction.down:
            current_direction_index = 2
        elif self.snake.direction == Direction.left:
            current_direction_index = 3

        sensor_front = self.sensors[current_direction_index]
        sensor_right = self.sensors[current_direction_index + 1]
        sensor_left = self.sensors[current_direction_index - 1]

        sensor_front_out = self.__output_normalized__(sensor_front.distance_to_obstacle())
        sensor_right_out = self.__output_normalized__(sensor_right.distance_to_obstacle())
        sensor_left_out = self.__output_normalized__(sensor_left.distance_to_obstacle())

        return np.array([sensor_front_out, sensor_right_out, sensor_left_out])

    def get_food_inputs(self):
        food_x = self.food.position[0]
        food_y = self.food.position[1]
        head_x = self.snake.head().position[0]
        head_y = self.snake.head().position[1]
        food_x_out = self.__output_normalized__(food_x - head_x)
        food_y_out = self.__output_normalized__(food_y - head_y)

        return np.array([food_x_out, food_y_out])

    def get_tail_inputs(self):
        tail_x = self.snake.tail().position[0]
        tail_y = self.snake.tail().position[0]
        head_x = self.snake.head().position[0]
        head_y = self.snake.head().position[1]
        tail_x_out = self.__output_normalized__(tail_x - head_x)
        tail_y_out = self.__output_normalized__(tail_y - head_y)

        return np.array([tail_x_out, tail_y_out])

    def __output_normalized__(self, output):
        # For object right in front of snake, output must be one
        if output == 0:
            output = 1      # In case tail_x == head_x for example

        if output < 0:
            normal_out = -(self.box.size() - (-output - 1)) / self.box.size()
        else:
            normal_out = (self.box.size() - (output - 1)) / self.box.size()

        return normal_out

    #  (2 - (-1 + 1))/2


    def update(self, individual_index):
        self.snake = self.snake_list[individual_index]
        self.network = self.network_list[individual_index]

        for sensor in self.sensors:
            sensor.update_snake(self.snake)

    def reset(self):
        pass
