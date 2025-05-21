from src.Classes.edf import EDF
from sklearn.pipeline import Pipeline

class Model:

    edfs: list[EDF] = []
    features: list[tuple] = []
    labels: list[str] = []
    pipeline: Pipeline | None

    def __init__(self, name):
        self.name = name
        self.pipeline = None
