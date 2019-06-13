from snake import Snake
from snakegame import Game
from genetic_algorithm import GeneticAlgorithm
from neural_network import NeuralNetwork
from player_ai_genetic import PlayerAIGenetic
import numpy as np


class GeneticGame(Game):

    def __init__(self,
                 inputs=7, outputs=3, hidden_layers=[],
                 population_size = 20, fittest_percent=0.2, mutation_chance=0.05, crossover_points=1,
                 screen_size=20, delay=200, box_width=20, score_tracking=False):

        self.population_size = population_size
        self.epochs = 0
        self.current_individual_index = 0

        self.snake_list = []
        self.network_list = []
        self.fitness_list = np.zeros(self.population_size)

        self.algorithm = GeneticAlgorithm(fittest_percent, mutation_chance, crossover_points)
        for i in range(self.population_size):
            self.network_list.append(NeuralNetwork(inputs, outputs, hidden_layers))

        super().__init__(screen_size, delay, box_width, True, score_tracking)

    def play(self):
        self.snake.start()

        if not self.snake.is_dead():

            if self.check_player_quit():
                pass

            self.get_player_move()
            self.move()
            self.check_food()
            self.score.refresh()

            # Kill snake if score reaches 0 (requiers initial score)
            if self.score.score == 0:
                self.snake_death()

        else:
            self.next_individual()

        self.draw()

    def get_fitness(self):
        self.snake.reset()
        self.fitness_list[self.current_individual_index] = self.score.score

    def next_individual(self):
        self.current_individual_index += 1

        if self.current_individual_index == self.population_size:
            self.end_epoch()
        else:
            self.get_fitness()
            self.update_snake()

            self.snake.reset()

        self.partial_reset()

    def end_epoch(self):
        self.epochs += 1
        self.generate_new_population()
        self.new_epoch()

    def new_epoch(self):
        self.current_individual_index = 0
        self.update_snake()

    def update_snake(self):
        self.snake = self.snake_list[self.current_individual_index]
        self.player.update(self.current_individual_index)

    def generate_new_population(self):
        pop_weights = []

        for net in range(len(self.network_list)):
            pop_weights.append(self.network_list[net].weights_to_array())

        new_pop = self.algorithm.generate_new_population(pop_weights, self.fitness_list)

        for net in range(len(self.network_list)):
            self.network_list[net].array_to_weights(new_pop[net])

    def setup_game(self):
        for i in range(self.population_size):
            self.snake_list.append(self.spawn_snake((self.__screen_size__//2, self.__screen_size__//2), self.game_box))

        self.snake = self.snake_list[0]
        self.food = self.spawn_food()
        self.player = PlayerAIGenetic(self.snake_list, self.food, self.game_box, self.network_list)

    def partial_reset(self):
        self.game_box.reset()
        self.__hit__ = False
        self.food = self.spawn_food()
        self.score.reset()
        self.player.reset()

    def reset(self):
        super().reset()
        self.snake_list.clear()
        self.network_list.clear()
        self.snake = self.snake_list[0]


if __name__ == "__main__":
    game = GeneticGame(delay=0, hidden_layers=[8, 8], mutation_chance=0.5)
    game.run()
