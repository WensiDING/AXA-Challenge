import numpy as np
import pandas as pd
from os import listdir

parametersPath = '/Users/ding_wensi/Documents/AXA-Challenge/training_parameters1.csv'
inputPath = '/Users/ding_wensi/Documents/AXA-Challenge/pred_data_v2/'
paths = listdir(inputPath)
labels = [f.split("_")[0] for f in paths]
paths = [inputPath + f for f in paths]


#submission = pd.read_table(predictionPath, encoding='utf-8')
parameters = pd.read_table(parametersPath, encoding='utf-8', sep=',')
for i in range(len(labels)):
    assign_data = pd.read_table(paths[i], encoding='utf-8', sep=',')
    row = parameters[parameters.iloc[:, 0] == labels[i]]
    theta = row.iloc[0, 1:]
    for j in range(assign_data.shape[0]):
        data = np.array(assign_data.iloc[j, 3:])
        assign_data.iloc[j, 0] = sum(theta[1:] * data) + theta[0]
    assign_data.to_csv(paths[i])
