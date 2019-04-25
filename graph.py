

class Node:

    def __init__(self, position, f):
        self.position = position
        self.f = f
        self.open_list = []
        self.closed_list = []

    def add_edge(self, node):
        self.open_list.append(node)

    def add_open_list(self, open_list):
        self.open_list = open_list

    def add_closed_edge(self, node):
        self.closed_list.append(node)

    def get_path(self):
        if len(self.closed_list) != 0:
            return self.closed_list[len((self.closed_list))-1]

        return None

    def get_available_edges(self):
        edges = []
        for edge in self.open_list:
            if not(edge in self.closed_list):
                edges.append(edge)

        return edges

    def get_lowest_f(self):
        if len(self.open_list) == 0:
            return None

        edge = self.open_list[0]
        for new_edge in self.open_list:
            if new_edge.f < edge.f:
                edge = new_edge

        return edge


class Graph:

    def __init__(self, root):
        self.graph = []
        self.root = root

    def add_edge(self, move, adjacent):
        self.graph.append(adjacent)
