from snake import Snake
from snakegame import Game
from genetic_algorithm import GeneticAlgorithm
from neural_network import NeuralNetwork
from player_ai_genetic import PlayerAIGenetic
import numpy as np
import pygame


class GeneticGame(Game):

    def __init__(self,
                 inputs=7, outputs=3, hidden_layers=[],
                 population_size = 20, fittest_percent=0.2, mutation_chance=0.05, crossover_points=1,
                 screen_size=20, delay=200, box_width=20,
                 food_value=200, moves_to_decrement=1, score_decrement=2, score_increment=2,
                 score_decrement_move=2, turn_decrement_factor=1.5, initial_score=100, score_tracking=False):

        self.population_size = population_size
        self.generation = 0
        self.current_individual_index = 0
        self.decrement_factor = turn_decrement_factor

        self.snake_list = []
        self.network_list = []
        self.fitness_list = np.zeros(self.population_size)

        self.algorithm = GeneticAlgorithm(fittest_percent, mutation_chance, crossover_points)
        for i in range(self.population_size):
            self.network_list.append(NeuralNetwork(inputs, outputs, hidden_layers))

        super().__init__(screen_size=screen_size, delay=delay, box_width=box_width, human_player=False,
                         food_value=food_value, moves_to_decrement=moves_to_decrement, score_decrement=score_decrement,
                         score_increment=score_increment, initial_score=initial_score, score_tracking=score_tracking,
                         score_decrement_move=score_decrement_move, turn_decrement_factor=turn_decrement_factor)

    def play(self):
        self.snake.start()

        if not self.snake.is_dead():

            self.check_player_input()

            move = self.get_player_move()

            self.check_penalties(move)

            self.move()
            self.check_food()
            self.score.refresh(turned=self.turned)

            # Kill snake if score reaches 0 (requiers initial score)
            if self.score.score == 0:
                self.score.score = 0
                self.snake_death()

        else:
            self.next_individual()

        self.draw()

    def check_penalties(self, move):
        if self.is_move_towards_food(move):
            self.score.score_increment()
        else:
            self.score.score_decrement()

        if self.check_collision(self.new_position(move)):
            self.score.ate_itself()

        if self.check_wall_hit(self.new_position(move)):
            self.score.hit_wall()

    def get_fitness(self):
        fitness = self.score.get_final_score()
        self.fitness_list[self.current_individual_index] = fitness

    def next_individual(self):
        self.get_fitness()

        self.current_individual_index += 1
        if self.current_individual_index == self.population_size:
            print("Generation " + str(self.generation) + " finished")
            self.end_epoch()
            return

        self.partial_reset()
        self.update_snake()

    def check_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.is_running = False

        if keys[pygame.K_UP]:
            self.__delay__ += 10
        elif keys[pygame.K_DOWN]:
            self.__delay__ -= 10
            if self.__delay__ < 0:
                self.__delay__ = 0

        pygame.event.clear()

    def end_epoch(self):
        self.generate_new_population()
        self.partial_reset()
        self.new_epoch()

    def new_epoch(self):
        self.generation += 1
        self.current_individual_index = 0

    def update_snake(self):
        self.snake = self.snake_list[self.current_individual_index]
        self.snake.reset()
        self.player.update(self.current_individual_index, self.food)

    def generate_new_population(self):
        pop_weights = []

        for net in range(len(self.network_list)):
            pop_weights.append(self.network_list[net].weights_to_array())

        new_pop = self.algorithm.generate_new_population(pop_weights, self.fitness_list)
        print(np.count_nonzero(self.fitness_list == 0)) #  TODO remove
        self.fitness_list.fill(0)

        for net in range(len(self.network_list)):
            self.network_list[net].array_to_weights(new_pop[net])

    def setup_game(self):
        for i in range(self.population_size):
            self.snake_list.append(self.spawn_snake((self.__screen_size__//2, self.__screen_size__//2), self.game_box))

        self.snake = self.snake_list[0]
        self.food = self.spawn_food()
        self.player = PlayerAIGenetic(self.snake_list, self.food, self.game_box, self.network_list)

    def is_move_towards_food(self, move):
        new_position = self.new_position(move)
        current_distance = self.manhattan(self.snake.head().position, self.food.position)
        new_distance = self.manhattan(new_position, self.food.position)

        if new_distance < current_distance:
            return True
        return False

    @staticmethod
    def manhattan(start, end):
        return abs(end[0] - start[0]) + abs(end[1] - start[1])

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
    game = GeneticGame(delay=0, hidden_layers=[4, 4], mutation_chance=0.05, fittest_percent=0.2, population_size=80,
                       crossover_points=2, inputs=7, food_value=500,
                       moves_to_decrement=1, score_decrement=3, screen_size=20, score_increment=2,
                       box_width=20, initial_score=500, turn_decrement_factor=1.25, score_decrement_move=2)
    game.run()
