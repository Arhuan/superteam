import numpy as np

class LinearRegression:

    def __init__(self, lammy=1):
        self.lammy = lammy

    def fit(self, X, y):
        n, d = X.shape

        self.w = np.zeros(d)

        

    def predict(self, X):
        return X@self.w 
