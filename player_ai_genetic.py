from player_ai import PlayerAI
from genetic_algorithm import GeneticAlgorithm
from neural_network import NeuralNetwork


class PlayerAIGenetic(PlayerAI):

    def __init__(self, snake, food, score, box):
        super().__init__(snake, food, score, box)

        self.algorithm = GeneticAlgorithm(fittest_percent, mutation_chance, crossover_points)
        self.network = NeuralNetwork(inputs, outputs, hidden_layers)

    def get_move(self):
        pass

    def reset(self):
        pass
