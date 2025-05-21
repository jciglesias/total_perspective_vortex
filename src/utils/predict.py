from src.Classes.edf import EDF
from sklearn.pipeline import Pipeline
import streamlit as st
from src.utils.utils import prepare_epochs_labels_for_pipeline


def predict(pipeline: Pipeline, edfs: list[EDF]):
    """
    Predict the labels for the given raw data using the trained pipeline.
    """
    if pipeline is None:
        return None
    try:
        x, labels = prepare_epochs_labels_for_pipeline(edfs)
        predictions = pipeline.predict(x)
        equals = [a == y for a, y in zip(predictions, labels)]
        table = {
            "Epochs": range(1, len(predictions) + 1),
            "Prediction": predictions,
            "Truth": labels,
            "equals": equals,
        }
        return table
    except Exception as e:
        st.error(f"Error predicting: {e}")
        return None