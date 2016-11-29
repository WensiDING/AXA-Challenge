from os import listdir
import numpy as np
from sklearn.model_selection import train_test_split
from predict import predict
from computeCostreg import computeCostreg
from computeGradreg import computeGradreg
from sklearn.svm import SVR
import scipy.optimize as op

outputPath = '/Users/ding_wensi/Documents/AXA-Challenge/training_result2.txt'
mypath = '/Users/ding_wensi/Documents/AXA-Challenge/data_v2/'
files = listdir(mypath)
files = files[1:]
paths = [mypath + f for f in files]
assignment = [f.split("_")[0] for f in files]
ll = len(assignment)

with open(outputPath, "a", encoding='utf-8') as myfile:
    for i in range(ll):
        data = np.loadtxt(paths[i], delimiter=',', skiprows=1)
        # # The first column contains the true results and the rest columns
        # # contains the features.
        X = data[:, 1:]
        y = data[:, 0]
        # train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        n = X_train.shape[0]
        m = X_train.shape[1]
        K = np.ones((n, m + 1))
        K[:, 1:] = X_train
        l = 1.0
        # Initialize unknown parameters
        initial_theta = np.ones((m + 1, 1))
        # Run minimize() to obtain the optimal theta
        x, f, d = op.fmin_l_bfgs_b(computeCostreg, initial_theta,
                                   args=(K, y_train, l), fprime=computeGradreg)
        theta = x
        n = X_test.shape[0]
        F = np.ones((n, m + 1))
        F[:, 1:] = X_test
        # Compute accuracy on the training set
        p = predict(theta, F)
        y_dif = y_test - p
        error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
        message = 'prediction error of ' + \
            assignment[i] + " is " + str(error) + '\n'
        myfile.write(message)

        X = data[:, 1:]
        y = data[:, 0]
        n = X.shape[0]
        m = X.shape[1]
        K = np.ones((n, m + 1))
        K[:, 1:] = X
        l = 0.0
        initial_theta = np.ones((m + 1, 1))
        x, f, d = op.fmin_l_bfgs_b(computeCostreg, initial_theta,
                                   args=(K, y, l), fprime=computeGradreg)
        message = 'theta of ' + assignment[i] + ' are ' + str(x) + '\n'
        myfile.write(message)
