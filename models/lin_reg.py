import numpy as np

class LinearRegression:

    def __init__(self, lammy=1):
        self.lammy = lammy

    def objective_fun(self, X, y, w):
        yXw = y * X * w
        print(-yXw)

        return np.sum(np.log(1.0 + np.exp(-yXw)))

    def fit(self, X, y):
        n, d = X.shape

        self.w = np.zeros(d)
        
        print(self.objective_fun(X, y, self.w))
        

    def predict(self, X):
        return X@self.w 
