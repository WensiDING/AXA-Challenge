from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uni
from sklearn.base import BaseEstimator
from sklearn.grid_search import RandomizedSearchCV
from os import listdir
import numpy as np
import xgboost as xgb

tuned_params = {'maxDepth': sp_randint(
    5, 25), 'eta': sp_uni.rvs(), 'num_round': sp_randint(50, 150)}

input_path = 'D:/3A/ML/project/AXA-wensi/data_xgboost_v1/CAT_dataset_v1.csv'
outputPath = 'D:/3A/ML/project/AXA-wensi/training_random_search_v1.txt'

with open(outputPath, "a") as myfile:

    class xgboost(BaseEstimator):
        def __init__(self, maxDepth=10, eta=0.6, num_round=100):
            self.maxDepth = maxDepth
            self.eta = eta
            self.num_round = num_round

        def expBiasObj(preds, dtrain):
            labels = dtrain.get_label()
            grad = -alpha * np.exp(alpha * (labels - preds)) + alpha
            hess = alpha**2 * np.exp(alpha * (labels - preds))
            return grad, hess

        def evalerror(preds, dtrain):
            labels = dtrain.get_label()
        # return a pair metric_name, result
            return 'error', np.mean(np.exp(alpha * (labels - preds)) - alpha * (labels - preds) + 1)

        def fit(self, X, y):
            param = {'max_depth': self.max_depth,
                     'eta': self.eta, 'silent': 1}
            watchlist = [(X, 'train')]
            bst = xgb.train(param, X, self.num_round, watchlist,
                            self.expBiasObj, self.evalerror)
            self.bst = bst
            return self

        def score(self, X, y):
            predict = self.bst.predict(X)
            dif = y - predict
            exp_error = -np.mean(np.exp(0.1 * dif) - 0.1 * dif - 1)
            self.score_ = exp_error
            return self.score_

    X = xgb.DMatrix(input_path)
    y = X.get_label()
    num_iter = 10
    num_cv = 5
    gs = RandomizedSearchCV(xgboost(), tuned_params,
                            n_iter=num_iter, cv=num_cv, refit=False)
    gs.fit(X, y)
    for i in range(num_iter):
        myfile.write(str(gs.grid_scores_[i].mean_validation_score) + '\n')
    myfile.write(str(gs.grid_scores_))
