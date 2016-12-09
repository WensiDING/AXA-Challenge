import numpy as np
from sklearn.model_selection import train_test_split
from predict import predict
from computeCostreg import computeCostreg
from computeGradreg import computeGradreg
from sklearn.svm import SVR
import scipy.optimize as op

# # Load the dataset

data = np.loadtxt(
    'D:/3A/ML/project/AXA-wensi/data_v2/Tech. Axa_dataset_v2.csv', delimiter=',', skiprows=1)


# # The first column contains the true results and the rest columns
# # contains the features.
X = data[:, 1:]
y = data[:, 0]

# train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

n = X_train.shape[0]
m = X_train.shape[1]

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
y_rbf = svr_rbf.fit(X_train, y_train).predict(X_test)

y_dif = y_test - y_rbf
exp_error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
mse_error = np.mean(y_dif ** 2)

print ('exp-error: ', exp_error)
print ('mse-error: ', mse_error)

# K = np.ones((n, m + 1))
# K[:, 1:] = X_train
# l = 0.0

# # Initialize unknown parameters
# initial_theta = np.ones((m + 1, 1))

# # Run minimize() to obtain the optimal theta
# x, f, d = op.fmin_l_bfgs_b(computeCostreg, initial_theta,
#                            args=(K, y_train, l), fprime=computeGradreg)

# theta = x

# n = X_test.shape[0]
# F = np.ones((n, m + 1))
# F[:, 1:] = X_test
# # Compute accuracy on the training set
# p = predict(theta, F)
# y_dif = y_test - p
# error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
# print(error)
# print(max(y_dif))
# p = predict(theta, K)
# y_dif = y_train - p
# error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
# print(error)
# print(max(y_dif))
# print("error : ", computeCostreg(np.array(theta), F, y_test, 0))
