from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from src.Classes.edf import EDF
from src.utils.utils import prepare_epochs_labels_for_pipeline

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
            ('scaler', StandardScaler()),
            ('pca', PCA()), 
            ('classifier', RandomForestClassifier())
        ])

        x, y = prepare_epochs_labels_for_pipeline(edfs)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.3, random_state=42)
