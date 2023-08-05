from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from tflearn import DNN, fully_connected, input_data, regression

from inz.utils import vector2onehot


def use_sklearn(x_train, y_train, x_test, y_test):
    model = MLPClassifier()
    model.fit(x_train, y_train)
    return model.score(x_test, y_test)


LOG_DIR = Path(__file__).parent.parent / 'log'
TENSORBOARD_DIR = LOG_DIR / 'model'
CHECKPOINT_PATH = LOG_DIR / 'checkpoint'
MODEL_FILE = LOG_DIR / 'model_weights'


def use_tflearn(x_train, y_train, x_test, y_test):
    net = input_data(shape=[None, x_train.shape[1]], name='input')
    net = fully_connected(net, 24, activation='sigmoid', bias_init='normal')
    net = fully_connected(net, 16, activation='sigmoid', bias_init='normal')
    net = fully_connected(net, 12, activation='sigmoid', bias_init='normal')
    net = fully_connected(net, 8, activation='sigmoid', bias_init='normal')
    net = regression(net)
    model = DNN(net,
                tensorboard_dir=TENSORBOARD_DIR.as_posix(),
                tensorboard_verbose=3,
                best_checkpoint_path=CHECKPOINT_PATH.as_posix())
    model.fit(x_train, y_train,
              validation_set=(x_test, y_test),
              n_epoch=100,
              batch_size=10,
              show_metric=True,
              run_id='DNN-4f')
    model.save(MODEL_FILE.as_posix())
    return model


def get_data(num_features=20):
    X = pd.read_csv('../data/data.csv')
    y = X.pop('Choroba')

    sel = SelectKBest(chi2, num_features).fit(X, y)
    sup = sel.get_support()

    X = X.drop(X.columns[~sup], axis=1)

    X['Choroba'] = y

    return X.values


def main():
    np.random.seed(42)

    data = get_data(4)

    train, test = train_test_split(data)
    print(train.shape, test.shape)

    x_train = train[:, :-1]
    y_train = train[:, -1] - 1
    y_train = vector2onehot(y_train)
    x_test = test[:, :-1]
    y_test = test[:, -1] - 1
    y_test = vector2onehot(y_test)
    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    # print(use_sklearn(x_train, y_train, x_test, y_test))
    print(use_tflearn(x_train, y_train, x_test, y_test))


if __name__ == '__main__':
    main()
