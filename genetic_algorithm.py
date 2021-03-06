
import numpy as np


class GeneticAlgorithm:

    def __init__(self, fittest_percent=0.2, mutation_chance=0.05, crossover_points=1):

        self.fittest_percent = fittest_percent          # Percentage of population selected as mating pool
        self.mutation_chance = mutation_chance
        self.crossover_points = crossover_points

        self.generation = 0

        # Setting a seed from /udev
        np.random.seed()

    def generate_new_population(self, population, fitness):

        assert len(population) == len(fitness)

        population_size = len(population)
        genome_size = len(population[0])
        fittest, fittest_fitness = self.select_fittest(population, fitness)

        # Number of children created
        offspring_size = population_size - len(fittest)
        offspring = np.empty(offspring_size*genome_size).reshape(offspring_size, genome_size)

        for i in range(offspring_size):
            parents = self.select_parents(fittest, fittest_fitness)

            # Executes crossover and mutates
            offspring[i] = self.mutate(self.crossover(*parents))

        new_population = np.concatenate((fittest, offspring))

        return new_population

    # Fittest proportionate
    @staticmethod
    def select_parents(fittest, fitness):
        pop_size = len(fittest)
        genome_size = len(fittest[0])

        fitness_copy = np.copy(fitness)

        parents = np.empty(2*genome_size).reshape(2, genome_size)

        for parent in range(2):
            fitness_sum = np.sum(fitness_copy)
            choice = np.random.rand() * fitness_sum
            current_sum = 0

            for i in range(pop_size):

                current_sum += fitness_copy[i]

                if choice < current_sum:
                    parents[parent] = fittest[i]
                    fitness_copy[i] = 0
                    break

        return parents

    def select_fittest(self, population, fitness):
        assert len(population) == len(fitness)

        population_size = len(population)
        genome_size = len(population[0])
        fittest_size = int(np.ceil(population_size*self.fittest_percent))
        fitness_copy = np.copy(fitness)

        fittest = np.empty(fittest_size*genome_size).reshape(fittest_size, genome_size)
        fittest_fitness = np.empty(fittest_size)

        for i in range(fittest_size):
            # Gets the index of the maximum fitness
            max_fitness_index = np.where(fitness_copy == np.amax(fitness_copy))[0][0]

            fittest[i] = population[max_fitness_index]
            fittest_fitness[i] = fitness[max_fitness_index]
            fitness_copy[max_fitness_index] = -np.inf

        return fittest, fittest_fitness

    def mutate(self, genome):

        mutated_genome = genome

        for gene in range(len(genome)):

            # Choose genes to mutate based on mutation chance
            choice = np.random.rand()
            if self.mutation_chance >= choice:

                mutated_gene = (np.random.rand() * 2 - 1)*100
                # mutated_gene = np.random.normal(genome[gene])
                mutated_genome[gene] = mutated_gene

        return mutated_genome

    def crossover(self, genome_a, genome_b):

        assert len(genome_a) == len(genome_b)

        # Distance between each crossover point
        crossover_delta = int(np.floor(len(genome_a)/(self.crossover_points + 1)))
        crossover_delta = 1 if crossover_delta < 1 else crossover_delta

        crossover_genome = genome_a

        for i in range(self.crossover_points):
            crossover_index = (i+1) * crossover_delta

            if i % 2 == 0:
                crossover_genome = np.concatenate((crossover_genome[0:crossover_index], genome_b[crossover_index:]))
            else:
                crossover_genome = np.concatenate((crossover_genome[0:crossover_index], genome_a[crossover_index:]))

        return crossover_genome
