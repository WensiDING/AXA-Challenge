import numpy as np
from sklearn.model_selection import train_test_split
#from sklearn.neural_network import MLPRegressor
#from computeCostreg import computeCostreg
#from sklearn.tree import DecisionTreeRegressor
#from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
# # Load the dataset
data = np.loadtxt(
    '/Users/ding_wensi/Documents/AXA-Challenge/data_v1/Tech. Axa_dataset.csv', delimiter=',', skiprows=1)


# # The first column contains the true results and the rest columns
# # contains the features.
X = data[:, 1:]
y = data[:, 0]

# train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

regressor = SVR(max_iter=20000000, C=0.1, epsilon=1, kernel='sigmoid')
regressor.fit(X_train, y_train)

pred = regressor.predict(X_test)

y_dif = y_test - pred
error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
print(max(y_dif))
print(error)
y_dif = y_train - regressor.predict(X_train)
error = np.mean(np.exp(0.1 * y_dif) - 0.1 * y_dif - 1)
print(error)
print(max(y_dif))
