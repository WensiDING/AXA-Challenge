import numpy as np


def computeGradreg(theta, X, y, l):
    # Computes the gradient of the cost with respect to the parameters.

    m = X.shape[0]  # number of training examples

    grad = np.zeros_like(theta)  # initialize gradient
    y_pred = np.dot(X, theta)
    y_dif = y - y_pred
    # ====================== YOUR CODE HERE ======================
    # Instructions: Compute the gradient of cost for each theta,
    # as described in the assignment.

    grad[0] = np.sum(np.exp(0.1 * y_dif) * (-0.1 * X[:, 0]) + 0.1 * X[:, 0])
    for i in range(1, len(theta)):
        grad[i] = np.sum(np.exp(0.1 * y_dif) * (-0.1 * X[:, i]
                                                ) + 0.1 * X[:, i]) + l * theta[i]
    grad = grad / m

    # =============================================================

    return grad
