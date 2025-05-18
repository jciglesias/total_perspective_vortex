import streamlit as st
from src.utils.filter_data import load_data, get_epochs_and_labels


def predict(pipeline, subject, task):
    """
    Predict the labels for the given raw data using the trained pipeline.
    """
    edfs = load_data(subject, task)
    predictions = []
    labels = []
    for edf in edfs:
        if edf.epochs is None:
            edf.epochs, edf.labels = get_epochs_and_labels(edf.raw)
        x = edf.epochs.get_data().flatten().reshape(1, -1)
        prediction = pipeline.predict(x)
        predictions += prediction[0].tolist()
        labels += edf.labels.tolist()
    equals = [x == y for x, y in zip(predictions, labels)]
    table = {
        "Epochs": range(1, len(predictions) + 1),
        "Prediction": predictions,
        "Truth": labels,
        "Equals": equals,
    }
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(
            table,
            hide_index=True,
        )
    with col2:
        correct = sum(equals)
        total = len(equals)
        st.metric(
            label="Accuracy",
            value=f"{correct}/{total}",
            delta=f"{correct / total:.2%}",
        )
    st.toast("Prediction completed!")