from player_ai import PlayerAI
from a_star import AStar


class PlayerAIAStar(PlayerAI):

    def __init__(self, snake, food, score, box, wall_list):
        super().__init__(snake, food, score, box, wall_list)

        self.obstacle_list = []
        self.a_star = AStar(box)