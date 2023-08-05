import matplotlib.pyplot as plt
import numpy as np

from sdnn import activation
from sdnn.data_generator import generate_data
from sdnn.utils import split

# np.random.seed(42)


class Perceptron:
    def __init__(self):
        self.w = np.random.rand(3, 1) - .5

    def fit(self, x, d, n_epoch=1001, batch_size=64):
        xlen = len(x)
        assert xlen == len(d), 'Features and labels must have the same length'

        x = np.c_[[-1] * xlen, x]
        print(x[:4, :])

        errors = []
        for epoch in range(n_epoch):
            if epoch % 100 == 0:
                self.plot(x, d)

            p = np.random.permutation(xlen)
            epoch_error = 0

            for batch_x, batch_y in zip(split(x[p], batch_size), split(d[p], batch_size)):
                w0 = self.w
                print(w0, 'epoch', epoch)

                y = self.predict(batch_x)
                err = batch_y - y
                epoch_error += np.sum(np.abs(err))
                update = batch_x.T @ err
                w = w0 + update
                self.w = w

            print('epoch_error:', epoch_error)
            errors.append(epoch_error)

            if epoch_error == 0:
                break

        fig, ax = plt.subplots(1, 2)
        ax[0].grid()
        ax[0].plot(range(len(errors)), errors)
        self.plot(x, d, ax[1])
        plt.show()

    def predict(self, x):
        xw = x @ self.w
        return activation.binary_step(xw)

    def plot(self, x, y, ax=plt):
        ax.grid()

        _, x1min, x2min = x.min(0) - 1
        _, x1max, x2max = x.max(0) + 1
        ax.axis([x1min, x1max, x2min, x2max])

        # plot data
        c1 = x[y.astype(bool).T[0]]
        c2 = x[~y.astype(bool).T[0]]

        ax.scatter(c1[:, 1], c1[:, 2], marker='^')
        ax.scatter(c2[:, 1], c2[:, 2], marker='v')

        # plot weights
        bias, w1, w2 = self.w.T[0]
        ax.quiver((x1max + x1min) / 2, (x2max + x2min) / 2, w1, w2, angles='xy', scale_units='xy', scale=1)

        def get_x2(x1):
            return (-w1 * x1 + bias) / w2

        ax.plot([-100, 100], [get_x2(-100), get_x2(100)], c='k')
        if ax is plt:
            plt.show()

    def __str__(self):
        return f'Perceptron: {self.w}'


def main():
    c1 = generate_data(100, 1, 0, 2 + 5)
    c2 = generate_data(100, 0, -2, -2 + 5)

    data = np.array([*c1, *c2])
    np.random.shuffle(data)

    x = data[:, :-1]
    y = data[:, -1].reshape(-1, 1)

    # x = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
    # y = np.array([0, 0, 1, 0]).reshape(-1, 1)

    print(x.shape)
    print(y.shape)

    p = Perceptron()
    p.fit(x, y, n_epoch=1001)


if __name__ == '__main__':
    main()
