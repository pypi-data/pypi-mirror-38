""" Module contains common functions used in project. """
from itertools import islice
from typing import Iterable, Union

import numpy as np
import pandas as pd

from .layers import Layer


def old_split(iterable: Iterable, width: int, allow_missing=True):
    """ Generator yields iterable in parts.

    :param iterable: iterable to split
    :param width: length of each part
    :param allow_missing: if True last part may be smaller
    """
    it = iter(iterable)
    flag = True
    while flag:
        retval = []
        flag = False
        for _ in range(width):
            try:
                retval.append(next(it))
            except StopIteration:
                if not allow_missing:
                    return
                break
        else:
            flag = True

        if not retval:
            return

        if isinstance(iterable, np.ndarray):
            retval = np.array(retval)

        yield retval


def split(iterable: Iterable, width: int, allow_missing=True):
    """ Generator yields iterable in parts.

    :param iterable: iterable to split
    :param width: length of each part
    :param allow_missing: if True last part may be smaller
    """
    it = iter(iterable)
    while True:
        retval = list(islice(it, width))

        if not retval:
            return
        if len(retval) != width and not allow_missing:
            return

        if isinstance(iterable, np.ndarray):
            retval = np.array(retval)

        yield retval


def iter_layers(network: Layer, attr, with_values=True, i=0):
    if network is None:
        return
    if i == 0:
        print()
        print(attr)
    values = getattr(network, attr)
    previous = network.previous

    shape = values.shape if values is not None else None
    print('Layer: {}, i: {} {}.shape: {}'.format(network.id, i, attr, shape))
    if with_values:
        print(values)
    iter_layers(previous, attr, with_values, i + 1)


def get_loss(pred, y) -> np.ndarray:
    return np.sum((pred - y) ** 2) / 2


def get_accuracy(pred, y):
    axis_ = np.argmax(pred, axis=1) - np.argmax(y, axis=1)
    return 1 - np.count_nonzero(axis_) / len(y)


def vector2onehot(vector: np.ndarray):
    unique = len(set(vector))
    length = len(vector)
    data = np.zeros((length, unique))
    data[range(length), vector] = 1
    return data


def chi2(X: np.ndarray, y: np.ndarray):
    """https://pl.wikipedia.org/wiki/Test_zgodno%C5%9Bci_chi-kwadrat#Zliczenia"""

    Y = vector2onehot(y - 1)
    observed = Y.T @ X  # n_classes * n_features

    feature_count = X.sum(axis=0).reshape(1, -1)
    class_prob = Y.mean(axis=0).reshape(-1, 1)
    expected = class_prob @ feature_count

    val = (observed - expected) ** 2 / expected
    return val.sum(axis=0)


def select_k_best(X, y, func=chi2, k=10, indices=False):
    scores = func(X, y)
    mask = np.zeros_like(scores, dtype=bool)
    args = np.argsort(scores)[-k:]
    if indices:
        return args
    mask[args] = 1
    return mask


def train_test_split(*arrays, test_size=.25, shuffle=True, seed: Union[int] = None):
    if seed is not None:
        np.random.seed(seed)

    n = len(arrays[0])
    order = np.random.permutation(n) if shuffle else np.arange(n)
    k = int(np.ceil(n * test_size))
    order_train = order[:-k]
    order_test = order[-k:]
    l = []
    for i in arrays:
        l.append(i[order_train])
        l.append(i[order_test])
    return l


def get_data(num_features=20):
    X = pd.read_csv('./data/data.csv')
    y = X.pop('Choroba')

    sup = select_k_best(X.values, y.values, k=num_features)

    X = X.drop(X.columns[~sup], axis=1)

    X['Choroba'] = y

    return X.values
