import numpy as np

class LinearRegression:

    def __init__(self, lammy=1):
        self.lammy = lammy

    def objective(self, X, y, w):
        yXw = y * X * w

        return np.sum(np.log(1.0 + np.exp(-yXw)))

    def gradient(self, X, y, w):
        yXw = y * X * w
        res = - y / (1.0 + np.exp(yXw))

        return X.T.dot(res)

    def fit(self, X, y):
        n, d = X.shape

        self.w = np.zeros(d)
        
        print(self.objective(X, y, self.w))
        print(self.gradient(X, y, self.w))
        

    def predict(self, X):
        return X@self.w 
