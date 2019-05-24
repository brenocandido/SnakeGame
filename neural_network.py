import numpy as np


class NeuralNetwork:

    def __init__(self, inputs, outputs, hidden_layers=[]):

        np.random.seed()

        self.weights = []

        # Generating layers weights
        previous_layer_nodes = inputs
        for i in range(len(hidden_layers)):
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
                weight = nodes_w[j]

                # Use softmax if outputting
                if i == len(self.weights) - 1:
                    output[j] = self.softmax(self.perceptron(x, weight))

                # Use sigmoid
                else:
                    output[j] = self.sigmoid(self.perceptron(x, weight))

        return output

    def set_weights(self, weights, layer):

        self.weights[layer] = weights

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


def main():
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 0, 1])

    epochs = 1000
    a = 0.1

    nn = NeuralNetwork(2, 1)
    # nn.set_weights([1, 1], 0)

    # print(x[0])
    # print('\n')
    # print(nn.weights[0])
    # print('\n')
    # print(np.dot(x[0], nn.weights[0]))

    for n in range(epochs):
        for i in range(len(x)):
            y_predict = nn.think(x[i])[0]
            e = y[i] - y_predict

            w_d = np.zeros(2)
            for j in range(len(nn.weights[0])):
                w_d[j] = a*x[i][j]*e

            nn.set_weights(nn.weights+w_d, 0)

    # print(nn.think([0, 1]))
    print(nn.weights)


main()
