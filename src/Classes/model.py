import numpy as np
from pandas import DataFrame
from src.Classes.edf import EDF
from src.Classes.feature_extractor import FeatureExtractor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

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
            ('clf', KNeighborsClassifier()),
        ])

    
    def train(self):
        """
        Train the model using the provided EDF data.
        """
        if not self.is_trained:
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
            self.pipeline.fit(self.x_train, self.y_train)
            self.is_trained = True
    
    def predict(self):
        predictions = self.pipeline.predict(self.x_test)
        equals = [a == y for a, y in zip(predictions, self.y_test)]
        table = {
            "Epochs": range(1, len(predictions) + 1),
            "Prediction": predictions,
            "Truth": self.y_test,
            "equals": equals,
        }
        return table
    
    def score(self):
        """
        Score the model using cross-validation.
        """
        columns = ["fold_1", "fold_2", "fold_3", "fold_4", "fold_5"]
        df = DataFrame([], columns=columns)
        for i in range(5):
            x_train, x_test, y_train, y_test = train_test_split(self.x_train, self.y_train, test_size=0.2, random_state=i)
            scores = cross_val_score(self.pipeline, x_train, y_train, cv=5)
            df.loc[i] = scores
        return df
