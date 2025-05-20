from src.utils.filter_data import get_epochs_and_labels
from src.Classes.edf import EDF
import numpy as np
from sklearn.pipeline import Pipeline


def predict(pipeline: Pipeline, edfs: list[EDF]):
    """
    Predict the labels for the given raw data using the trained pipeline.
    """
    x = []
    labels = []
    for edf in edfs:
        if edf.training:
            continue
        if edf.epochs is None:
            edf.epochs, edf.labels = get_epochs_and_labels(edf.raw)
        x.append(edf.epochs.get_data())
        labels += edf.labels.tolist()
    x = np.array(x)
    x = [x.flatten() for x in x]
    try:
        predictions = pipeline.predict(x)[0]
        equals = [a == y for a, y in zip(predictions, labels)]
        table = {
            "Epochs": range(1, len(predictions) + 1),
            "Prediction": predictions,
            "Truth": labels,
            "equals": equals,
        }
        return table
    except Exception as e:
        return None