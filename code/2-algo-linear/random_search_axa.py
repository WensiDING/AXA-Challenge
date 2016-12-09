import time
import pandas as pd
import numpy as np
from computeCostreg import computeCostreg
from computeGradreg import computeGradreg
import scipy.optimize as op
from scipy.stats import randint as sp_randint
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV

paths = np.array(('/Users/ding_wensi/Documents/AXA-Challenge/data_v1/Tech. Axa_dataset_v1.csv',
                  '/Users/ding_wensi/Documents/AXA-Challenge/data_v2/Tech. Axa_dataset_v2.csv', '/Users/ding_wensi/Documents/AXA-Challenge/data_v3/Tech. Axa_dataset_v3.csv'))
outputPath = '/Users/ding_wensi/Documents/AXA-Challenge/random_search_srv_v4.txt'

tuned_params = {'ll': np.arange(0.0, 1, 0.1)}

with open(outputPath, "a") as myfile:
    class Modele_svr(BaseEstimator):
        def __init__(self, ll=0.1):
            self.ll = ll

        def svr(self, X, y):
            n = X.shape[0]
            m = X.shape[1]
            K = np.ones((n, m + 1))
            K[:, 1:] = X
            # Initialize unknown parameters
            initial_theta = np.ones((m + 1, 1))
            # Run minimize() to obtain the optimal theta
            x, f, d = op.fmin_l_bfgs_b(computeCostreg, initial_theta, args=(
                K, y, self.ll), fprime=computeGradreg)
            return x

        def fit(self, X, y):
            self.theta = self.svr(X, y)
            return self

        def score(self, X, y):
            n = X.shape[0]
            m = X.shape[1]
            K = np.ones((n, m + 1))
            K[:, 1:] = X
            self.score_ = - computeCostreg(self.theta, K, y, 0)
            return self.score_

    gs = GridSearchCV(Modele_svr(), tuned_params, cv=10)
    data = np.loadtxt(paths[1], delimiter=',', skiprows=1)
    X = data[:, 1:]
    y = data[:, 0]
    gs.fit(X, y)
    myfile.write(str(gs.cv_results_))
