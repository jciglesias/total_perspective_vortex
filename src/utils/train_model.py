import streamlit as st
from src.Classes.model import Model
import streamlit as st
from sklearn.model_selection import cross_val_score
from pandas import DataFrame

def score_model(model: Model):
    """
    Train a model using the provided EDF data.
    """
    with st.spinner("Scoring the model...", show_time=True):
        try:
            columns = ["fold_1", "fold_2", "fold_3", "fold_4", "fold_5"]
            df = DataFrame([], columns=columns)
            for i in range(5):
                scores = cross_val_score(model.pipeline, model.x_train, model.y_train, cv=5)
                df.loc[i] = scores
            return df

        except Exception as e:
            st.error(f"Error scoring the model: {e}")
            return None

def train_model(model: Model):
    """
    Train a model using the provided EDF data.
    """
    with st.spinner("Training the model...", show_time=True):
        try:
            if not model.is_trained:
                model.pipeline.fit(model.x_train, model.y_train)
                model.is_trained = True

        except Exception as e:
            st.error(f"Error training the model: {e}")
            return None