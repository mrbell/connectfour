import sys
import json
import random
import numpy as np


def sigmoid(z):
    """
    Return the sigmoid function evaluated at the given input.

    :param z: Vector or scalar input.
    :return: Sigmoid of the given input.
    """
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """
    Derivative of the sigmoid evaluated at the given input.

    :param z: Input vector or scalar.
    :return:
    """
    return np.exp(-z) * sigmoid(z) ** 2


class CrossEntropyCost(object):

    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)))

    @staticmethod
    def delta(z, a, y):
        return a - y


class QuadraticCost(object):

    @staticmethod
    def fn(a, y):
        return 0.5*np.linalg.norm(a-y)**2

    @staticmethod
    def delta(z, a, y):
        return (a - y) * sigmoid_prime(z)


class TDNN(object):
    """
    Following the example here:
        http://neuralnetworksanddeeplearning.com/
    """

    def __init__(self, nodes_per_layer):
        self.num_layers = len(nodes_per_layer)
        self.nodes_per_layer = nodes_per_layer
        self.biases = None
        self.weights = None
        self.default_weight_initializer()

        self.total_grad_b = None
        self.total_grad_w = None
        self.last_result = None
        self.total_delta_b = None
        self.total_delta_w = None

    def default_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.nodes_per_layer[1:]]
        # Normalized Gaussian distributed weights
        self.weights = [np.random.randn(y, x) / np.sqrt(x)
                        for x, y in zip(self.nodes_per_layer[:-1], self.nodes_per_layer[1:])]

    def large_weight_initializer(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def predict(self, a):
        """
        Predict outputs for the given input.

        :param a: An input vector.
        :return: A vector of outputs.
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def start_game(self):
        self.total_grad_w = None
        self.total_grad_b = None
        self.last_result = None
        self.total_delta_w = None
        self.total_delta_b = None

    def partial_update(self, x, y, eta, lmbda):
        # TODO: All of these need to loop over the different layers of the weights
        # QUESTION: What to do about biases exactly?
        y_next = y
        y_last = self.last_result

        grad_b, grad_w = self.backprop(x, y)

        if y_last is None:
            self.total_grad_b = grad_b
            self.total_grad_w = grad_w
            self.total_delta_b = [np.zeros(b.shape) for b in grad_b]
            self.total_delta_w = [np.zeros(w.shape) for w in grad_w]
        else:
            self.total_delta_w += -eta * (y_next - y_last) * self.total_grad_w
            self.total_delta_b += -eta * (y_next - y_last) * self.total_grad_b  # TODO: Check this
            self.total_grad_w = [gw + lmbda * tgw for gw, tgw in zip(grad_w, self.total_grad_w)]
            self.total_grad_b = [gb + lmbda * tgb for gb, tgb in zip(grad_b, self.total_grad_b)]  # TODO: Check this

        self.last_result = y

    def update_mini_batch(self, x, y, eta, lmbda, n):
        """

        :param mini_batch:
        :param eta:
        :param lmbda:
        :param n:
        :return:
        """
        nabla_b, nabla_w = self.backprop(x, y)

        self.weights = [(1 - eta * (lmbda / n)) * w - eta * nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x]  # list to store all the activations, layer by layer
        zs = []  # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost.delta(zs[-1], activations[-1], y)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return nabla_b, nabla_w

    def save(self, filename):
        """

        :param filename:
        :return:
        """

        data = {
            "sizes": self.sizes,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases]
        }
        with open(filename, 'w') as f:
            json.dump(data, f)


def load(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    net = TDNN(data["sizes"])
    net.weights = [np.array(w) for w in data['weights']]
    net.biases = [np.array(b) for b in data['biases']]

    return net