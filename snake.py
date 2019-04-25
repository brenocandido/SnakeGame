from enum import Enum
import game_box
from game_box import Item


class Direction(Enum):
    up = -1
    right = -2
    down = 1
    left = 2
    none = 0


class State(Enum):
    idle = 0
    running = 1
    dead = 2


class Body:
    def __init__(self, coordinate):
        self.position = coordinate

    def sum_y(self, amount):
        self. position = (self.position[0], self.position[1] + amount)

    def sum_x(self, amount):
        self.position = (self.position[0] + amount, self.position[1])


class Snake:
    def __init__(self, position, box):
        self.direction = Direction.up
        self.state = State.idle
        self.body = []
        self.box = box
        self.initial_spawn(position)
        self.size_up = False
        self.__starting_position__ = position

    def initial_spawn(self, position):
        self.body.append(Body(position))
        self.box.set_item(position, Item.head)
        self.body.append(Body((position[0],position[1]+1)))
        self.box.set_item(position, Item.body)

    def head(self):
        return self.body[len(self.body) - 1]

    def body_following_head(self):
        return self.body[len(self.body) - 2]

    def tail(self):
        return self.body[0]

    def turn(self, direction):
        if direction != Direction.none:
            self.direction = direction

    def eat(self):
        self.size_up = True

    def kill(self):
        self.state = State.dead

    def start(self):
        if self.state == State.idle:
            self.state = State.running

    def is_moving(self):
        return self.state == State.running

    def is_dead(self):
        return self.state == State.dead

    def move_head(self, position):
        self.body.append(Body(position))
        self.box.set_item(position, Item.head)
        self.box.set_item(self.body_following_head().position, Item.body)

    def decrease_size(self):
        self.box.set_item(self.body[0].position, Item.empty)
        del self.body[0]

    def reset(self):
        self.state = State.idle
        self.direction = Direction.up
        self.body = []
        self.initial_spawn(self.__starting_position__)
        self.size_up = False
