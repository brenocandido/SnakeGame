import numpy as np
from genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt


class NeuralNetwork:

    def __init__(self, inputs, outputs, hidden_layers=[]):

        np.random.seed()
        self.weights = []
        self.hidden_layers_number = len(hidden_layers)
        self.total_layers_number = self.hidden_layers_number + 1
        # Numbers of nodes of hidden layers + inputs
        self.nodes_number = sum(hidden_layers) + inputs

        # Generating layers weights
        previous_layer_nodes = inputs
        for i in range(self.hidden_layers_number):
            self.weights.append(np.random.random((hidden_layers[i], previous_layer_nodes)))
            previous_layer_nodes = hidden_layers[i]

        # Appending last layer weights before output
        self.weights.append(np.random.random((outputs, previous_layer_nodes)))

    def think(self, inputs):
        assert len(inputs) == len(self.weights[0][0])

        x = inputs
        output = inputs
        for i in range(len(self.weights)):
            nodes_w = self.weights[i]
            output = np.empty(len(nodes_w))

            for j in range(len(nodes_w)):
                weights = nodes_w[j]

                # Use softmax if outputting
                # if i == len(self.weights) - 1:
                #     output[j] = self.softmax(self.perceptron(x, weights))
                # Use sigmoid
                # else:
                #     output[j] = self.sigmoid(self.perceptron(x, weights))

                output[j] = self.perceptron(x, weights)

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
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def perceptron(inputs, weights):
        dot = np.dot(inputs, weights)
        return dot

    @staticmethod
    def softmax(z):
        s = np.exp(z.T) / np.sum(np.exp(z.T)).reshape(-1, 1)

        return s

# TODO remove this part after testing is done
def main():
    x = np.array([4, -2, 1, 3])

    epochs = 1000

    net_input = 4
    net_output = 1
    net_hidden_layer = [3]
    ga = GeneticAlgorithm()

    pop_size = 50

    nn = []
    for i in range(pop_size):
        nn.append(NeuralNetwork(net_input, net_output, net_hidden_layer))

    fitness_array = []
    out_print = []

    for n in range(epochs):
        fitness = np.empty(len(nn))
        out_array = np.empty(len(nn))
        pop_weights = []

        for net in range(len(nn)):
            out = nn[net].think(x)[0]
            fitness[net] = -((out - 50000)**2)
            out_array[net] = out
            pop_weights.append(nn[net].weights_to_array())

        fit_mean = fitness.mean()
        out_mean = out_array.mean()

        fitness_array.append(fit_mean)
        out_print.append(out_mean)

        pop_weights = np.array(pop_weights)
        new_pop = ga.generate_new_population(pop_weights, fitness)

        for net in range(len(nn)):
            nn[net].array_to_weights(new_pop[net])

    plt.plot(out_print)
    plt.show()


main()
