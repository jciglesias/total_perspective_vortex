import streamlit as st
from src.Classes.model import Model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from src.utils.utils import prepare_epochs_labels_for_pipeline
from sklearn.model_selection import cross_val_score

def train_model(model: Model):
    """
    Train a model using the provided EDF data.
    """
    with st.spinner("Training the model...", show_time=True):
        try:
            scores = cross_val_score(model.pipeline, model.x_train, model.y_train, cv=5)
            if not model.is_trained:
                model.pipeline.fit(model.x_train, model.y_train)
                model.is_trained = True
            return scores

        except Exception as e:
            st.error(f"Error training the model: {e}")
            return None