

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

    def get_available_nodes(self, move_list):
        nodes = []
        closed_list_positions = self.get_node_positions(self.closed_list)
        move_list_positions = self.get_node_positions(move_list)
        for node in self.open_list:
            if node.position not in closed_list_positions and node.position not in move_list_positions:
                nodes.append(node)

        return nodes

    @staticmethod
    def get_node_positions(node_list):
        node_positions = []
        for node in node_list:
            node_positions.append(node.position)

        return node_positions

    def get_lowest_f(self, move_list):
        available_list = self.get_available_nodes(move_list)
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
