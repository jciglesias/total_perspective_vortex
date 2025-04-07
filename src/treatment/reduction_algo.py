from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from src.data.Subject import Subject

def reduction_algo(n_components: int) -> Pipeline:
    pca = PCA(n_components=n_components)
    return Pipeline([
        ('reduce_dim', pca),
        ('lr', LogisticRegression())
    ])