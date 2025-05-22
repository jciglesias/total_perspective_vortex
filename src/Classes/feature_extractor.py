from sklearn.base import BaseEstimator, TransformerMixin
from src.utils.utils import extract_features
from numpy import array

class FeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for epoch in X:
            features.append(extract_features(epoch))
        return array(features)