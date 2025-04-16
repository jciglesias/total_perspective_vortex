import streamlit as st
import src.utils as ut
from time import sleep
from src.filter_data import load_data
from src.train_model import train_model

def predict():
    pass

subjects = ut.subjects
subject = st.selectbox(
    label="Select a subject",
    options=subjects,
    index=0,
)
tasks = ut.tasks.keys()
task = st.selectbox(
    label="Select a task",
    options=tasks,
    index=0,
)

is_loaded = f"{subject}_{task}_loaded" in st.session_state
is_trained = f"{subject}_{task}_pipeline" in st.session_state
load_tab, train_tab, predict_tab = st.tabs(["Load data", "Train model", "Predict"])
with load_tab:
    if is_loaded:
        st.write("Data already loaded.")
    else:
        st.session_state[f"{subject}_{task}_loaded"] = load_data(subject, task)
with train_tab:
    if is_trained:
        st.write("Model already trained.")
    else:
        st.session_state[f"{subject}_{task}_pipeline"] = train_model(st.session_state[f"{subject}_{task}_loaded"])
with predict_tab:
    st.write("Predicting...")
    predict()