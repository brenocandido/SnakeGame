
import numpy as np


class GeneticAlgorithm:

    def __init__(self, fittest_percent=0.5, mutation_chance=0.05, crossover_points=1):

        self.fittest_percent = fittest_percent          # Percentage of population selected as mating pool
        self.mutation_chance = mutation_chance
        self.crossover_points = crossover_points

        self.generation = 0

        # Setting a seed from /udev
        np.random.seed()

    def select_fittest(self, population, fitness):
        assert len(population) == len(fitness)

        population_size = len(population)
        fittest_size = int(population_size*self.fittest_percent)

        fittest = np.empty(fittest_size)

    def mutate(self, genome):

        mutated_genome = genome

        for gene in range(len(genome)):

            # Choose genes to mutate based on mutation chance
            choice = np.random.random()
            if self.mutation_chance >= choice:

                mutated_gene = np.random.normal(genome[gene])
                mutated_genome[gene] = mutated_gene

        return mutated_genome

    def crossover(self, genome_a, genome_b):

        assert len(genome_a) == len(genome_b)

        # Distance between each crossover point
        crossover_delta = int(np.floor(len(genome_a)/(self.crossover_points + 1)))
        assert crossover_delta >= 1

        crossover_genome = genome_a

        for i in range(self.crossover_points):
            crossover_index = (i+1) * crossover_delta

            if i % 2 == 0:
                crossover_genome = np.concatenate((crossover_genome[0:crossover_index], genome_b[crossover_index:]))
            else:
                crossover_genome = np.concatenate((crossover_genome[0:crossover_index], genome_a[crossover_index:]))

        return crossover_genome


a = np.array([1., 2., 3., 4., 5.])
b = np.array([6., 7., 8., 9., 10.])
ga = GeneticAlgorithm(1, mutation_chance=0.05, crossover_points=1)
crossover = ga.crossover(a, b)
print(crossover)
mutation = ga.mutate(crossover)
print(mutation)

