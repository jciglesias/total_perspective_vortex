from mne.io import BaseRaw
from mne import Epochs
import numpy as np

class EDF:
    raw: BaseRaw
    filtered: BaseRaw | None
    epochs: Epochs | None
    labels: np.ndarray | None
    raw_image: str | None
    filtered_image: str | None
    training: bool | None
    filename: str | None

    def __init__(self, raw: BaseRaw):
        self.raw = raw
        self.filtered = None
        self.epochs = None
        self.labels = None
        self.raw_image = None
        self.filtered_image = None
        self.training = None
        self.filename = None
