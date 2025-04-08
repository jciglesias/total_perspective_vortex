import streamlit as st
import src.utils as ut
from time import sleep
from src.filter_data import load_data, filter_data

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

# files = ut.get_file_name(subject, task)
is_trained = st.toggle(label="Train model", value=False)
if is_trained:
    placeholder = st.empty()
    with placeholder.container():
        col_1, col_2 = st.columns(2)
        col_1.write("Raw data")
        col_2.write("Filtered data")
        for raw, fig in load_data(subject, task):
            with col_1:
                st.pyplot(fig)
            with col_2:
                st.pyplot(filter_data(raw, 13, 30).plot())
        st.write("Data loaded successfully!")
    with placeholder.container():
        train_model()
        st.write("Model trained successfully!")
    if st.button("Predict"):
        st.balloons()
else:
    st.write("Model not trained")