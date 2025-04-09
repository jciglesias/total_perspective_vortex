import streamlit as st
import src.utils as ut
from time import sleep
from src.filter_data import load_data, filter_data

def empty_load_data(subject, task):
    col_1, col_2 = st.columns(2)
    col_1.write("Raw data")
    col_2.write("Filtered data")
    for raw, fig in load_data(subject, task):
        with col_1:
            st.pyplot(fig)
        with col_2:
            st.pyplot(filter_data(raw, 13, 30).plot())
    st.write("Data loaded successfully!")

def train_model():
    st.write("Training model...")
    sleep(5)
    st.write("Model trained successfully!")

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

# files = ut.get_file_name(subject, task)
# is_trained = st.toggle(label="Train model", value=False)
is_trained = f"{subject}_{task}" in st.session_state
col_1, col_2 = st.columns(2)
with col_1:
    train_button = st.button("Train model", disabled=is_trained)
if train_button:
    placeholder = st.empty()
    with placeholder.container():
        empty_load_data(subject, task)
    with placeholder.container():
        st.session_state[f"{subject}_{task}"] = train_model()
    st.rerun()
with col_2:
    predict_button = st.button("Predict", disabled=not is_trained)
if predict_button:
    st.write("Predicting...")
    predict()