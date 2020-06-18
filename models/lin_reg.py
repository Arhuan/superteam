import numpy as np
from numpy.linalg import solve

class LinearRegression:
    def fit(self, X, y):
        self.w = solve(X.T@X, X.T@y)
    
    def predict(self, X):
        return X@self.w 
