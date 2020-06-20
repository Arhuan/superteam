import numpy as np

class LinearRegression:
    def gaussian_rbf_kernel(self, X1, X2, sigma=0.5):
        n, d = np.shape(X1)
        t, d = np.shape(X2)
        K = np.zeros((n, t))
        for i in range(n):
            for j in range(t):
                K[i, j] = np.exp(-1 * np.linalg.norm(X1[i] - X2[j])**2 / (2 * sigma**2))
        return K

    def fit(self, X, y):
        X = np.c_[X, np.ones(X.shape[0])]
        self.X = X
        K = self.gaussian_rbf_kernel(X, X)
        self.w = np.linalg.solve(K.T@K, K.T@y)
    
    def predict(self, X):
        X = np.c_[X, np.ones(X.shape[0])]
        K_test = self.gaussian_rbf_kernel(X, self.X)
        return K_test@self.w 
