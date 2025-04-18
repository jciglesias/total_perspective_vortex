import streamlit as st
import src.utils as ut
from time import sleep
from src.filter_data import load_data
from src.train_model import train_model

def show_data(image, raw, col):
    with col:
        st.image(image)
        st.write("Sampling Frequency:", raw.info['sfreq'])
        st.write("Number of Channels:", len(raw.info['ch_names']))
        st.write("Duration (s):", raw.times[-1])

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

# is_loaded = f"{subject}_{task}_filtered_raws" in st.session_state
is_trained = f"{subject}_{task}_pipeline" in st.session_state
if not f"{subject}_{task}_filtered_raws" in st.session_state:
    with st.container():
        st.session_state[f"{subject}_{task}_edfs"] = load_data(subject, task)
load_tab, train_tab, predict_tab = st.tabs(["Process data", "Train model", "Predict"])
with load_tab:
    col_l, col_r = st.columns(2)
    col_l.write("Raw data")
    col_r.write("Filtered data")
    for edf in st.session_state[f"{subject}_{task}_edfs"]:
        show_data(edf.raw_image, edf.raw, col_l)
        show_data(edf.filtered_image, edf.filtered, col_r)
with train_tab:
    if is_trained:
        st.write("Model already trained.")
    else:
        st.session_state[f"{subject}_{task}_pipeline"] = train_model(st.session_state[f"{subject}_{task}_edfs"])
with predict_tab:
    st.write("Predicting...")
