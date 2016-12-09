from os import listdir
import numpy as np
from sklearn.model_selection import train_test_split
from predict import predict
from computeCostreg import computeCostreg
from computeGradreg import computeGradreg
from sklearn.svm import SVR
import scipy.optimize as op
import pandas as pd
import numpy as np
outputPath = '/Users/ding_wensi/Documents/AXA-Challenge/tel/training_parameters.csv'
mypath = '/Users/ding_wensi/Documents/AXA-Challenge/tel/train_tel.csv'


data = np.loadtxt(mypath, delimiter=',', skiprows=1)
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
output = pd.Series(x)
output.to_csv(outputPath, encoding='utf-8')
