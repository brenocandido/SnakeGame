from player_ai import PlayerAI
from sensor import Sensor
from snakegame import Direction
from sensor import Item
import numpy as np


class PlayerAIGenetic(PlayerAI):

    def __init__(self, snake_list, food, box, network_list):

        super().__init__(snake_list[0], food, box)

        self.snake_list = snake_list
        self.network_list = network_list

        self.network = self.network_list[0]

        self.sensors = [Sensor(Direction.up, self.snake, self.box),
                        Sensor(Direction.up_right, self.snake, self.box),
                        Sensor(Direction.right, self.snake, self.box),
                        Sensor(Direction.down_right, self.snake, self.box),
                        Sensor(Direction.down, self.snake, self.box),
                        Sensor(Direction.down_left, self.snake, self.box),
                        Sensor(Direction.left, self.snake, self.box),
                        Sensor(Direction.up_left, self.snake, self.box)]

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
        food_horizontal = self.get_food_input_right_left()
        food_vertical = self.get_food_input_front_back()
        # tail = self.get_tail_inputs()
        return np.concatenate((sensors, food_horizontal, food_vertical))

    def get_sensors_inputs(self):
        current_direction_index = 0
        if self.snake.direction == Direction.right:
            current_direction_index = 2
        elif self.snake.direction == Direction.down:
            current_direction_index = 4
        elif self.snake.direction == Direction.left:
            current_direction_index = 6

        n_sensors = len(self.sensors)
        sensor_input_body = []
        sensor_input_wall = []

        for i in range(n_sensors):
            index = (current_direction_index + i) % n_sensors
            sensor = self.sensors[index]

            # If not sensor to the back of the snake
            if i != 4:
                sensor_input_body.append(self.__output_normalized__(sensor.distance_to_item(Item.body)))
                sensor_input_wall.append(self.__output_normalized__(sensor.distance_to_item(Item.wall)))

        return np.concatenate((sensor_input_wall, sensor_input_body))

    def get_food_inputs(self):
        return self.get_inputs_xy(self.food.position)

    def get_food_input_right_left(self):
        food = self.get_food_inputs()
        food_x = food[0]

        food_left = 0
        food_right = 0
        if food_x > 0:
            food_right = food_x
        else:
            food_left = abs(food_x)

        return food_right, food_left

    def get_food_input_front_back(self):
        food = self.get_food_inputs()
        food_y = food[1]

        food_front = 0
        food_back = 0
        if food_y > 0:
            food_front = food_y
        else:
            food_back = abs(food_y)

        return food_front, food_back

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
        #     normal_out = (self.box.size() - (output)) / self.box.size()
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
