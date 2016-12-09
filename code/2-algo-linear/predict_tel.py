import numpy as np
import pandas as pd

parametersPath = '/Users/ding_wensi/Documents/AXA-Challenge/tel/training_parameters.csv'
inputPath = '/Users/ding_wensi/Documents/AXA-Challenge/tel/pred_tel.csv'

parameters = pd.read_table(
    parametersPath, sep=',', header=None)

assign_data = pd.read_table(inputPath, sep=',')
theta = np.array(parameters.iloc[:, 1])
for j in range(assign_data.shape[0]):
    #data = np.array(assign_data.iloc[j, 3:])
    data = np.array(assign_data.iloc[j, 2:])
    assign_data.iloc[j, 0] = sum(theta[1:] * data) + theta[0]
assign_data.to_csv(inputPath, index=False)
