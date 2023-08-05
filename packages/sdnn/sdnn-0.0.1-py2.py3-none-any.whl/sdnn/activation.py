""" This module contains all activation functions.

source: https://en.wikipedia.org/wiki/Activation_function
"""

import numpy as np


def identity(x, der=False):
    if der:
        return 1
    return x


def binary_step(x, der=False):
    if der:
        if x == 0:
            raise ValueError('?')
        return 0

    return x >= 0


def sigmoid(x, der=False):
    if der:
        return np.exp(x) / (1 + np.exp(x)) ** 2
    return 1 / (1 + np.exp(-x))


def tanh(x, der=False):
    if der:
        return 1 - tanh(x) ** 2
    return np.tanh(x)


def arctan(x, der=False):
    if der:
        return 1 / (1 + x ** 2)
    return np.arctan(x)


def soft_sign(x, der=False):
    if der:
        return 1 / (1 + abs(x)) ** 2
    return x / (1 + abs(x))


def relu(x, der=False):
    if der:
        return x * (x > 0) / x
    return np.maximum(0, x)


def softmax(x):
    rows_max = np.max(x, axis=1).reshape(-1, 1)
    e_x = np.exp(x - rows_max)
    div = np.sum(e_x, axis=1).reshape(-1, 1)
    return e_x / div
