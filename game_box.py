from enum import Enum


class Item(Enum):
    empty = 0
    body = 1
    head = 2
    food = 3


class Field:
    def __init__(self, item=Item.empty):
        self.occupied = False
        self.item = item

    def set_occupied(self, boolean):
        self.occupied = boolean

    def set_item(self, item):
        self.item = item


class GameBox:

    def __init__(self, side_size):
        self.box = [[Field() for i in range(side_size)] for j in range(side_size)]
        self.side_size = side_size

    def is_occupied(self, position):
        return self.box[position[0]][position[1]].occupied

    def set_occupied(self, position, boolean, item=Item.empty):
        if not boolean: # Removing from position
            self.set_item(position, Item.empty)

        else: # Adding item
            self.set_item(position, item)

        self.box[position[0]][position[1]].set_occupied(boolean)

    def set_item(self, position, item):
        self.box[position[0]][position[1]].set_item(item)

    def get_unoccupied_list(self):
        unoccupied_list = []
        for i in range(self.side_size):
            for j in range(self.side_size):
                if not self.is_occupied((i, j)):
                    unoccupied_list.append((i, j))

        return unoccupied_list

    def reset(self):
        for i in range(self.side_size):
            for j in range(self.side_size):
                self.box[i][j].set_occupied(False)
