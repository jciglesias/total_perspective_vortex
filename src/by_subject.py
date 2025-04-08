import streamlit as st
import src.utils as ut
from time import sleep

def load_data(files):
    for file in files:
        st.write(f"Loading data from {file}")
        sleep(5)

def train_model():
    st.write("Training model...")
    sleep(5)
    st.write("Model trained successfully!")

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

files = ut.get_file_name(subject, task)
is_trained = st.toggle(label="Train model", value=False)
if is_trained:
    placeholder = st.empty()
    with placeholder.container():
        load_data(files)
        st.write("Data loaded successfully!")
    sleep(5)
    placeholder.empty()
    with placeholder.container():
        train_model()
        st.write("Model trained successfully!")
    if st.button("Predict"):
        st.balloons()
else:
    st.write("Model not trained")