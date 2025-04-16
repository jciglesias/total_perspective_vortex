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

is_loaded = f"{subject}_{task}_filtered_raws" in st.session_state
is_trained = f"{subject}_{task}_pipeline" in st.session_state
load_tab, train_tab, predict_tab = st.tabs(["Load data", "Train model", "Predict"])
with load_tab:
    col_l, col_r = st.columns(2)
    col_l.write("Raw data")
    col_r.write("Filtered data")
    if not is_loaded:
        load_data(subject, task)
    for raw, filtered in zip(st.session_state[f"{subject}_{task}_raws"], st.session_state[f"{subject}_{task}_filtered_raws"]):
        with col_l:
            st.pyplot(raw.plot())
            st.write("Sampling Frequency:", raw.info['sfreq'])
            st.write("Number of Channels:", len(raw.info['ch_names']))
            st.write("Duration (s):", raw.times[-1])
        with col_r:
            st.pyplot(filtered.plot())
            st.write("Sampling Frequency:", filtered.info['sfreq'])
            st.write("Number of Channels:", len(filtered.info['ch_names']))
            st.write("Duration (s):", filtered.times[-1])
with train_tab:
    if is_trained:
        st.write("Model already trained.")
    else:
        st.session_state[f"{subject}_{task}_pipeline"] = train_model(st.session_state[f"{subject}_{task}_filtered_raws"])
with predict_tab:
    st.write("Predicting...")
    predict()