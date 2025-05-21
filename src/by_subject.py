import streamlit as st
import src.utils.utils as ut
from src.utils.filter_data import load_data, read_raw_data
from src.utils.train_model import train_model
from src.utils.predict import predict
from pandas import DataFrame

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

if f"{subject}_{task}_model" not in st.session_state:
    with st.container():
        st.session_state[f"{subject}_{task}_model"] = load_data(subject, task)
load_tab, train_tab, predict_tab = st.tabs(["Process data", "Train model", "Predict"])
with load_tab:
    col_l, col_r = st.columns(2)
    col_l.write("Raw data")
    col_r.write("Filtered data")
    for edf in st.session_state[f"{subject}_{task}_model"].edfs:
        edf.raw_image = ut.create_image(edf.raw, f"{edf.filename}_raw_image.png")
        edf.filtered_image = ut.create_image(edf.filtered, f"{edf.filename}_filtered_image.png")
        show_data(edf.raw_image, edf.raw, col_l)
        show_data(edf.filtered_image, edf.filtered, col_r)
with train_tab:
    columns = ["fold_1", "fold_2", "fold_3", "fold_4", "fold_5"]
    df = DataFrame([], columns=columns)
    for i in range(5):
        scores = train_model(st.session_state[f"{subject}_{task}_model"])
        df.loc[i] = scores
    st.dataframe(
        df,
        column_config={
            "fold_1": st.column_config.NumberColumn(
                "Fold 1",
                help="Fold 1 score",
                format="percent",
            ),
            "fold_2": st.column_config.NumberColumn(
                "Fold 2",
                help="Fold 2 score",
                format="percent",
            ),
            "fold_3": st.column_config.NumberColumn(
                "Fold 3",
                help="Fold 3 score",
                format="percent",
            ),
            "fold_4": st.column_config.NumberColumn(
                "Fold 4",
                help="Fold 4 score",
                format="percent",
            ),
            "fold_5": st.column_config.NumberColumn(
                "Fold 5",
                help="Fold 5 score",
                format="percent",
            ),
        },
        hide_index=True
        )
    # st.write("Scores:", scores)
    # st.write("Mean Score:", scores.mean())    
with predict_tab:
    with st.spinner("Predicting...", show_time=True):
        table = predict(st.session_state[f"{subject}_{task}_model"])
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