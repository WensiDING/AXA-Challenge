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
outputPath = '/Users/ding_wensi/Documents/AXA-Challenge/training_parameters1.csv'
mypath = '/Users/ding_wensi/Documents/AXA-Challenge/data_v2/'
files = listdir(mypath)
files = files[1:]
paths = [mypath + f for f in files]
assignment = [f.split("_")[0] for f in files]
ll = len(assignment)
output = np.zeros((ll, 12))

for i in range(ll):
    data = np.loadtxt(paths[i], delimiter=',', skiprows=1)
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
    output[i, :] = x
output = pd.DataFrame(output, index=assignment)
output.to_csv(outputPath,encoding='utf-8')
