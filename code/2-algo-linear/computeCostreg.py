import numpy as np


def computeCostreg(theta, X, y, l):
    # Computes the cost of using theta as the parameter for regularized
    # logistic regression.

    m = X.shape[0]  # number of training examples
    y_pred = np.dot(X, theta)
    y_dif = y - y_pred
    J = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1) + \
        np.dot(theta[1:].T, theta[1:]) * (l / (2.0 * m))

    return J
