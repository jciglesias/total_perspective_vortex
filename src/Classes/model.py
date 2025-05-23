from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.decomposition import PCA
from src.Classes.edf import EDF
from src.Classes.feature_extractor import FeatureExtractor
import numpy as np

class Model:
    is_trained: bool = False
    edfs: list[EDF]
    pipeline: Pipeline
    x_train: list
    y_train: list
    x_test: list
    y_test: list

    def __init__(self, edfs: list[EDF]):
        self.edfs = edfs
        self.pipeline = Pipeline([
            ('features', FeatureExtractor()),
            ('scaler', StandardScaler()),
            ('reduce_dim', PCA()),
            # ('clf', RandomForestClassifier()),
            ('clf', KNeighborsClassifier()),
        ])

        x_train_shape = self.edfs[0].x_train.shape
        x_test_shape = self.edfs[0].x_test.shape
        self.x_train = np.empty(shape=(0, x_train_shape[1], x_train_shape[2]))
        self.x_test = np.empty(shape=(0, x_test_shape[1], x_test_shape[2]))
        self.y_train = np.empty(0)
        self.y_test = np.empty(0)
        for edf in self.edfs:
            self.x_train = np.concatenate((self.x_train, edf.x_train), axis=0)
            self.x_test = np.concatenate((self.x_test, edf.x_test), axis=0)
            self.y_train = np.concatenate((self.y_train, edf.y_train), axis=0)
            self.y_test = np.concatenate((self.y_test, edf.y_test), axis=0)
        print(f"x_train shape: {self.x_train.shape}")
        print(f"x_test shape: {self.x_test.shape}")
        print(f"y_train shape: {self.y_train.shape}")
        print(f"y_test shape: {self.y_test.shape}")
    
    def train(self):
        """
        Train the model using the provided EDF data.
        """
        if not self.is_trained:
            self.pipeline.fit(self.x_train, self.y_train)
            self.is_trained = True
    
    def predict(self, subject:str):
        x_test_shape = self.edfs[0].x_test.shape
        x_test = np.empty(shape=(0, x_test_shape[1], x_test_shape[2]))
        y_test = np.empty(0)
        for edf in self.edfs:
            if subject in edf.filename:
                x_test = np.concatenate((x_test, edf.x_test), axis=0)
                y_test = np.concatenate((y_test, edf.y_test), axis=0)
        predictions = self.pipeline.predict(x_test)
        equals = [a == y for a, y in zip(predictions, y_test)]
        table = {
            "Epochs": range(1, len(predictions) + 1),
            "Prediction": predictions,
            "Truth": y_test,
            "equals": equals,
        }
        return table

