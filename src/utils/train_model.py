import streamlit as st
from src.Classes.edf import EDF
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from src.utils.utils import prepare_epochs_labels_for_pipeline

def train_model(edfs: list[EDF]):
    """
    Train a model using the provided EDF data.
    """
    with st.spinner("Training the model...", show_time=True):
        # x = []
        # y = []
        # for edf in edfs:
        #     if not edf.training:
        #         continue
        #     if edf.epochs is None:
        #         edf.epochs, edf.labels = get_epochs_and_labels(edf.raw)
        #     x += edf.epochs.get_data()[:,0].tolist()
        #     y += edf.labels.tolist()

        # # x = np.array(x)
        # # x = [x.flatten() for x in x]

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier())
        ])

        try:
            x, y = prepare_epochs_labels_for_pipeline(edfs)
            pipeline.fit(x, y)

            return pipeline
        except Exception as e:
            st.error(f"Error training the model: {e}")
            st.write("Features:", x)
            return None