

class Node:

    def __init__(self, position, f):
        self.position = position
        self.f = f
        self.open_list = []
        self.closed_list = []

    def add_open_node(self, node):
        self.open_list.append(node)

    def add_open_list(self, open_list):
        self.open_list = open_list

    def add_closed_node(self, node):
        self.closed_list.append(node)

    def get_path(self):
        if len(self.closed_list) != 0:
            return self.closed_list[len((self.closed_list))-1]

        return None

    def get_available_nodes(self):
        nodes = []
        for node in self.open_list:
            if node not in self.closed_list:
                nodes.append(node)

        return nodes

    def get_lowest_f(self):
        available_list = self.get_available_nodes()
        if len(available_list) == 0:
            return None

        edge = available_list[0]
        for new_edge in available_list:
            if new_edge.f < edge.f:
                edge = new_edge

        return edge


class Graph:

    def __init__(self, root):
        self.graph = []
        self.root = root

    def add_edge(self, move, adjacent):
        self.graph.append(adjacent)
