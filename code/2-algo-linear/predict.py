import numpy as np


def predict(theta, X):
    # Predict whether the label is 0 or 1 using learned logistic
    # regression parameters theta. The threshold is set at 0.5

    m = X.shape[0]  # number of training examples

    c = np.zeros(m)  # predicted classes of training examples

    c = np.dot(X, theta)

    return c
