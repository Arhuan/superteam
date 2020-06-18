import numpy as np
from numpy.linalg import solve

class LinearRegression:
    def fit(self, X, y):
        X = np.c_[X, np.ones(X.shape[0])]
        self.w = solve(X.T@X, X.T@y)
    
    def predict(self, X):
        X = np.c_[X, np.ones(X.shape[0])]
        return X@self.w 
