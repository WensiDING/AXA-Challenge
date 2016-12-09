#!/usr/bin/python
from os import listdir
import numpy as np
import xgboost as xgb
###
# advanced: customized loss function
#
print ('start running gradient boost')

outputPath1 = 'D:/3A/ML/project/AXA-wensi/training_error_exp_v1.txt'
outputPath2 = 'D:/3A/ML/project/AXA-wensi/training_error_mse_v1.txt'
mypath = 'D:/3A/ML/project/AXA-wensi/data_xgboost_v1/'
files = listdir(mypath)
paths = [mypath + f for f in files]
assignment = [f.split("_")[0] for f in files]
ll = len(assignment)
message1 = list()
message2 = list()
alpha_small = 0.06
alpha = 0.1

for i in range(ll-1):
	print ('*' * 50)
	print (assignment[i])
	print ('*' * 50)
	dtrain = xgb.DMatrix(paths[i])
	# note: for customized objective function, we leave objective as default
	# note: what we are getting is margin value in prediction
	# you must know what you are doing
	param = {'max_depth': 10, 'eta': 0.6, 'silent': 1}
	num_round = 100
	watchlist = [(dtrain, 'train')]

	# user define objective function, given prediction, return gradient and second order gradient
	# this is log likelihood loss
	def expBiasObj(preds, dtrain):
		labels = dtrain.get_label()
		grad = -alpha * np.exp(alpha*(labels-preds)) + alpha
		hess = alpha**2 * np.exp(alpha*(labels-preds))
		return grad, hess 
	# user defined evaluation function, return a pair metric_name, result
	# NOTE: when you do customized loss function, the default prediction value is margin
	# this may make buildin evalution metric not function properly
	# for example, we are doing logistic loss, the prediction is score before logistic transformation
	# the buildin evaluation error assumes input is after logistic transformation
	# Take this in mind when you use the customization, and maybe you need write customized evaluation function

	def evalerror(preds, dtrain):
		labels = dtrain.get_label()
	    # return a pair metric_name, result
		return 'error', np.mean( np.exp(alpha*(labels-preds)) - alpha*(labels-preds) + 1 ) 

	# training with customized objective, we can also do step by step training
	# simply look at xgboost.py's implementation of train
	bst = xgb.train(param, dtrain, num_round, watchlist, expBiasObj, evalerror)

	# compute accuray on the training set
	predict = bst.predict(dtrain)
	labels = dtrain.get_label()
	dif = labels - predict
	exp_error = np.mean(np.exp(0.1 * dif) - 0.1 * dif - 1)
	mse_error = np.mean(dif ** 2)
	message1.append(str(exp_error) + '\n') 
	message2.append(str(mse_error) + '\n') 

################################################################
# for tel

def expBiasObj(preds, dtrain):
	labels = dtrain.get_label()
	grad = -alpha * np.exp(alpha*(labels-preds)) + alpha
	hess = alpha**2 * np.exp(alpha*(labels-preds))
	return grad, hess 

def expBiasObj_small(preds, dtrain):
	alpha = alpha_small
	labels = dtrain.get_label()
	grad = -alpha * np.exp(alpha*(labels-preds)) + alpha
	hess = alpha**2 * np.exp(alpha*(labels-preds))
	return grad, hess 

# user defined evaluation function, return a pair metric_name, result
# NOTE: when you do customized loss function, the default prediction value is margin
# this may make buildin evalution metric not function properly
# for example, we are doing logistic loss, the prediction is score before logistic transformation
# the buildin evaluation error assumes input is after logistic transformation
# Take this in mind when you use the customization, and maybe you need write customized evaluation function
def evalerror(preds, dtrain):
	labels = dtrain.get_label()
    # return a pair metric_name, result
	return 'error', float( np.sum(np.exp(alpha*(labels-preds)) - alpha*(labels-preds) + 1 )) / len(labels)

def evalerror_small(preds, dtrain):
	alpha = alpha_small
	labels = dtrain.get_label()
    # return a pair metric_name, result
	return 'error', float( np.sum(np.exp(alpha*(labels-preds)) - alpha*(labels-preds) + 1 )) / len(labels)

dtrain = xgb.DMatrix(paths[-1])

param = {'max_depth': 10, 'eta': 0.6, 'silent': 1}
num_round = 100
watchlist = [(dtrain, 'train')]
labels = dtrain.get_label()

bst = xgb.train(param, dtrain, num_round, watchlist, expBiasObj_small, evalerror_small)

ptrain = bst.predict(dtrain, output_margin=True)
dtrain.set_base_margin(ptrain)

print ('*'*50)
print ('this is result of running from initial prediction')
print ('*'*50)
param = {'max_depth': 10, 'eta': 0.6, 'silent': 1}
num_round = 100
watchlist = [(dtrain, 'train')]

bst = xgb.train(param, dtrain, num_round, watchlist, expBiasObj, evalerror)

# compute accuray on the training set
predict = bst.predict(dtrain)
dif = labels - predict
exp_error = np.mean(np.exp(0.1 * dif) - 0.1 * dif - 1)
mse_error = np.mean(dif ** 2)
message1.append(str(exp_error) + '\n') 
message2.append(str(mse_error) + '\n')


with open(outputPath1, "a") as myfile:
    for i in range(ll):
        myfile.write(message1[i])

with open(outputPath2, "a") as myfile:
    for i in range(ll):
        myfile.write(message2[i])

