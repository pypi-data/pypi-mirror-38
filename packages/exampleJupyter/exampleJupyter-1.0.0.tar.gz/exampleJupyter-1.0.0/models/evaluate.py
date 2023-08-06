import pandas as pd
import numpy as np
import scipy as sc
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.datasets import load_boston, load_iris
class Regressor():

    def __init__(self, estimator = None):
        if estimator:
            self.estimator = estimator
        else:
            self.estimator = LinearRegression()

    def fit(self, X, y):
        self.estimator.fit(X, y)

    def predict(self, X):
        return self.estimator.predict(X)

    def metric(self, y_real, y_pred):
        return np.sqrt(mean_squared_error(y_true=y_real, y_pred=y_pred))

class Classifier():

    def __init__(self, estimator = None):
        if estimator:
            self.estimator = estimator
        else:
            self.estimator = LogisticRegression()

    def fit(self, X, y):
        self.estimator.fit(X, y)

    def predict(self, X):
        return self.estimator.predict(X)

    def metric(self, y_real, y_pred):
        return classification_report(y_true=y_real, y_pred=y_pred)

class Reader():
    def __init__(self,  dataset = "boston", path=None, target_label = None , type = None):
        if path is not None and target_label is not None:
            if type == 'excel':
                df = pd.read_excel(path)
            elif type == 'json':
                df = pd.read_json(path)
            else:
                df = pd.read_csv(path)
            self.y = df[target_label].values
            self.target_name = target_label
            df.drop(target_label, axis=1, inplace=True)
            self.X = df.values
            self.feature_names = list(df.columns)
        elif dataset=='boston':
            boston = load_boston()
            self.X = boston['data']
            self.y = boston['target']
            self.target_name = 'Price'
            self.feature_names = boston['feature_names']
        elif dataset=='iris':
            iris = load_iris()
            self.X = iris['data']
            self.y = iris['target']
            self.target_name = 'Specie'
            self.feature_names = iris['feature_names']

    def get_data(self):
        return self.X, self.y, self.feature_names, self.target_name









