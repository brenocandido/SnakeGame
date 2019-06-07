from snakegame import Game
from genetic_algorithm import GeneticAlgorithm
from neural_network import NeuralNetwork


class GeneticGame(Game):

    def __init__(self,  inputs=8, outputs=3, hidden_layers=[],
                        population_size = 20, fittest_percent=0.2, mutation_chance=0.05, crossover_points=1,
                        screen_size=20, delay=200, box_width=20, score_tracking=False):
        super().__init__(screen_size, delay, box_width, human_player=False, score_tracking)

        self.population_size = population_size

        self.algorithm = GeneticAlgorithm(fittest_percent, mutation_chance, crossover_points)
        self.network = NeuralNetwork(inputs, outputs, hidden_layers)

    def setup_game(self):
        self.snake = []
        for i in range(self.population_size):
            self.snake.append(self.spawn_snake(self.__screen_size__//2, self.__screen_size__//2), self.game_box)



# if __name__ == "__main__":
    # game = GeneticGame(human_player=False, score_tracking=True)
    # game.run()