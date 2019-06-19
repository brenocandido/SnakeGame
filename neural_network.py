import numpy as np
from genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt


class NeuralNetwork:

    def __init__(self, inputs=7, outputs=3, hidden_layers=[]):

        np.random.seed()
        self.weights = []
        self.hidden_layers_number = len(hidden_layers)
        self.total_layers_number = self.hidden_layers_number + 1
        # Numbers of nodes of hidden layers + inputs
        self.nodes_number = sum(hidden_layers) + inputs

        # Generating layers weights
        previous_layer_nodes = inputs
        for i in range(self.hidden_layers_number):
            # Generates weights between -1 and 1
            self.weights.append((np.random.random((previous_layer_nodes, hidden_layers[i]))*2 - 1)*100)
            previous_layer_nodes = hidden_layers[i]

        # Appending last layer weights before output
        self.weights.append((np.random.random((previous_layer_nodes, outputs))*2 - 1)*100)

    def think(self, inputs):
        # assert len(inputs) == len(self.weights[0][0])

        x = inputs
        output = inputs
        for i in range(len(self.weights)):
            nodes_w = self.weights[i]

            # Use softmax if outputting
            if i == len(self.weights) - 1:
                output = self.softmax(self.perceptron(x, nodes_w))
            # Use sigmoid
            else:
                # output = self.sigmoid(self.perceptron(x, nodes_w))*2 - 1
                output = self.sigmoid(self.perceptron(x, nodes_w))
                # output = np.tanh(self.perceptron(x, nodes_w))

            x = output

        return output

    def set_layer_weights(self, weights, layer):
        assert len(self.weights[layer]) == len(weights)
        self.weights[layer] = np.array(weights)

    def set_node_weights(self, weights, layer, node):
        assert len(self.weights[layer][node]) == len(weights)
        self.weights[layer][node] = np.array(weights)

    def weights_to_array(self):
        weights_array = []

        for layer in range(len(self.weights)):
            for node in range(len(self.weights[layer])):
                for weight in range(len(self.weights[layer][node])):
                    weights_array.append(self.weights[layer][node][weight])

        return np.array(weights_array)

    def array_to_weights(self, array):
        k = 0

        for layer in range(len(self.weights)):
            for node in range(len(self.weights[layer])):
                for weight in range(len(self.weights[layer][node])):
                    self.weights[layer][node][weight] = array[k]
                    k += 1

    @staticmethod
    def sigmoid(x):
        return 1. / (1. + np.exp(-x))

    @staticmethod
    def perceptron(inputs, weights):
        dot = np.dot(inputs, weights)
        return dot

    @staticmethod
    def softmax(z):
        s = np.exp(z.T) / np.sum(np.exp(z.T)).reshape(-1, 1)

        return s


def main():
    x = np.array([0.5, 1, -1, -0.5])

    epochs = 1

    net_input = 4
    net_output = 3
    net_hidden_layer = [5, 3]
    ga = GeneticAlgorithm(fittest_percent=0.5, mutation_chance=0.01, crossover_points=1)

    pop_size = 50

    nn = []
    for i in range(pop_size):
        nn.append(NeuralNetwork(net_input, net_output, net_hidden_layer))

    fitness_array = []
    out_print = []
    out_print_mean = []

    for n in range(epochs):
        fitness = np.empty(len(nn))
        out_array = np.empty(len(nn))
        pop_weights = []
        max_fitness = -999999999
        max_fitness_index = 0

        for net in range(len(nn)):
            out = nn[net].think(x)[0]
            print(np.argmax(out))
        #     fitness[net] = -(0.1*out**4 + 1*out**3 - 1000*out**2 + 2)
        #     if fitness[net] > max_fitness:
        #         max_fitness = fitness[net]
        #         max_fitness_index = net
        #     out_array[net] = out
        #     pop_weights.append(nn[net].weights_to_array())
        #
        # fitness_array.append(fitness.mean())
        # out_print.append(out_array[max_fitness_index])
        # out_print_mean.append(out_array.mean())
        #
        # pop_weights = np.array(pop_weights)
        # new_pop = ga.generate_new_population(pop_weights, fitness)
        #
        # for net in range(len(nn)):
        #     nn[net].array_to_weights(new_pop[net])

    # plt.figure()
    # plt.subplot(211)
    # plt.plot(out_print)
    # plt.subplot(212)
    # plt.plot(out_print_mean)
    # plt.show()


if __name__ == "__main__":
    main()
