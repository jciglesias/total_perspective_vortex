from src.Classes.model import Model
import streamlit as st
from src.utils.utils import prepare_epochs_labels_for_pipeline


def predict(model: Model):
    """
    Predict the labels for the given raw data using the trained pipeline.
    """
    try:
        predictions = model.pipeline.predict(model.x_test)
        equals = [a == y for a, y in zip(predictions, model.y_test)]
        table = {
            "Epochs": range(1, len(predictions) + 1),
            "Prediction": predictions,
            "Truth": model.y_test,
            "equals": equals,
        }
        return table
    except Exception as e:
        st.error(f"Error predicting: {e}")
        return None