import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor

class Regressor():
    def __init__(self, saved_model):
        with open(saved_model, 'rb') as fp:
            self.clf = pickle.load(fp)
    def predict(self, fname):
        df = pd.read_excel(fname)
        X_pred = df.values
        y_pred = self.clf.predict(X_pred)
        df['CONS_PRED'] = y_pred
        return df
    def predict_and_save(self, fname):
        df = self.predict(fname)
        df.to_excel("out.xlsx")