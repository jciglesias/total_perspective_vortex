import streamlit as st
from src.Classes.model import Model
import src.utils.utils as ut
from src.utils.filter_data import load_data

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

if f"{subject}_{task}_model" not in st.session_state:
    with st.container():
        st.session_state[f"{subject}_{task}_model"] = Model(load_data(subject, task, st.session_state.folder_selected))
load_tab, train_tab, predict_tab = st.tabs(["Process data", "Train model", "Predict"])
with load_tab:
    col_l, col_r = st.columns(2)
    col_l.write("Raw data")
    col_r.write("Filtered data")
    for edf in st.session_state[f"{subject}_{task}_model"].edfs:
        if edf.raw_image is None:
            edf.raw_image = ut.create_image(edf.raw, f"{edf.filename}_raw_image.png")
        if edf.filtered_image is None:
            edf.filtered_image = ut.create_image(edf.filtered, f"{edf.filename}_filtered_image.png")
        col_l.image(edf.raw_image, use_container_width=True)
        col_r.image(edf.filtered_image, use_container_width=True)
with train_tab:
    model = st.session_state[f"{subject}_{task}_model"]
    model.train()
    df = model.score()
    st.write(f"Cross-validation mean score: {df.mean(axis=None).mean() * 100:.2f}%")
    st.dataframe(
        df,
        column_config=ut.cross_val_column_config,
        hide_index=True
        )   
with predict_tab:
    with st.spinner("Predicting...", show_time=True):
        table = st.session_state[f"{subject}_{task}_model"].predict()
        if table is None:
            st.write("No model trained yet.")
            st.stop()
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(
                table,
                hide_index=True,
            )
        with col2:
            correct = sum(table['equals'])
            total = len(table['equals'])
            st.metric(
                label="Accuracy",
                value=f"{correct}/{total}",
                delta=f"{correct / total:.2%}",
            )