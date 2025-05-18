import streamlit as st
from src.Classes.edf import EDF
from src.utils.filter_data import get_epochs_and_labels
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

def train_model(edfs: list[EDF]):
    """
    Train a model using the provided EDF data.
    """
    with st.spinner("Training the model...", show_time=True):
        # Extract features and labels from the EDF data
        x = []
        y = []
        for edf in edfs:
            if edf.epochs is None:
                edf.epochs, edf.labels = get_epochs_and_labels(edf.raw)
            x.append(edf.epochs.get_data())
            y.append(edf.labels)

        # Flatten the data
        x = [x.flatten() for x in x]

        # Create a pipeline with a scaler and a classifier
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier())
        ])

        # Train the model
        pipeline.fit(x, y)

        return pipeline