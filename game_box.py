from enum import Enum


class Item(Enum):
    empty = 0
    body = 1
    head = 2
    food = 3
    wall = 4


class Field:
    def __init__(self, item=Item.empty):
        self.item = item

    def set_item(self, item):
        self.item = item


class GameBox:

    def __init__(self, side_size):
        self.box = [[Field() for i in range(side_size)] for j in range(side_size)]
        self.side_size = side_size

    def size(self):
        return len(self.box)

    def is_occupied(self, position):
        return self.box[position[0]][position[1]].item != Item.empty

    def is_empty(self, position):
        return not self.is_occupied(position)

    def set_item(self, position, item):
        self.box[position[0]][position[1]].set_item(item)

    def get_unoccupied_list(self):
        unoccupied_list = []
        for i in range(self.side_size):
            for j in range(self.side_size):
                if not self.is_occupied((i, j)):
                    unoccupied_list.append((i, j))

        return unoccupied_list

    def is_obstacle(self, position):
        if self.box[position[0]][position[1]].item == Item.body:
            return True

        return False

    def is_in_box(self, position):
        if 0 <= position[0] < self.side_size and 0 <= position[1] < self.side_size:
            return True

        return False

    def item(self, position):
        return self.box[position[0]][position[1]].item

    def reset(self):
        for i in range(self.side_size):
            for j in range(self.side_size):
                if self.box[i][j].item != Item.wall:
                    self.box[i][j].set_item(Item.empty)
