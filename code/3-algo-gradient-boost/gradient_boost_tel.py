# -*- coding: utf8 -*-
import numpy as np
import xgboost as xgb
from os import listdir
import random
###
# advanced: customized loss function
#
print ('start running example to used customized objective function')


alpha = 0.06
alpha_large = 0.1
# user define objective function, given prediction, return gradient and second order gradient
# note: for customized objective function, we leave objective as default
# note: what we are getting is margin value in prediction
# you must know what you are doing
def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0-preds)
    return grad, hess

def expBiasObj(preds, dtrain):
	labels = dtrain.get_label()
	grad = -alpha * np.exp(alpha*(labels-preds)) + alpha
	hess = alpha**2 * np.exp(alpha*(labels-preds))
	return grad, hess 

def expBiasObj_large(preds, dtrain):
	alpha = alpha_large
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


def evalerror_large(preds, dtrain):
	alpha = alpha_large
	labels = dtrain.get_label()
    # return a pair metric_name, result
	return 'error', float( np.sum(np.exp(alpha*(labels-preds)) - alpha*(labels-preds) + 1 )) / len(labels)

path = './input_training/Telephonie_dataset_v3.csv'
dtrain = xgb.DMatrix(path+'.train')
dtest = xgb.DMatrix(path+'.test')
dmerge = path + '.merge'

labels = dtest.get_label()

param = {'max_depth': 10, 'eta': 0.6, 'silent': 1}
num_round = 100
watchlist = [(dtrain, 'train')]

# training with customized objective, we can also do step by step training
# simply look at xgboost.py's implementation of train
bst = xgb.train(param, dtrain, num_round, watchlist, expBiasObj, evalerror)

ptrain = bst.predict(dtrain, output_margin=True)
ptest = bst.predict(dtest, output_margin=True)
dtrain.set_base_margin(ptrain)
dtest.set_base_margin(ptest)

print ('*'*50)
print ('this is result of running from initial prediction')
print ('*'*50)
param = {'max_depth': 10, 'eta': 0.6, 'silent': 1}
num_round = 100
watchlist = [(dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist, expBiasObj_large, evalerror_large)

preds = bst.predict(dtest)
for i in range(len(preds)):
	if preds[i] < 0 :
		preds[i] = 0
with open(dmerge+'_new', 'w') as dest:
	for l in range(len(preds)):
		dest.write('%s\n' % preds[l]) 
dest.close()

print ('error=%f' % ( np.sum(np.exp(alpha*(labels-preds)) - alpha*(labels-preds) + 1 ) /float(len(preds))))

##prediction output
# with open(dmerge, 'r') as src:
# 	with open(dmerge+'_new', 'w') as dest:
# 		lines = src.readlines()
# 		if len(lines)-1 == len(preds):
# 			for l in range(len(preds)):
# 				dest.write('%s,%s\n' % (lines[l+1].rstrip('\n'), preds[l])) 
# src.close()
# dest.close()