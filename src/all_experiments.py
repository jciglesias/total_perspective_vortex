from src.utils.filter_data import load_data
from src.utils.predict import predict
from src.utils.train_model import train_model
from src.utils.utils import tasks, subjects
import streamlit as st

tasks_accuracies = {}
for task in tasks:
    tasks_accuracies[task] = []
    for subject in subjects:
        edfs = load_data(subject, task)
        if f"{subject}_{task}_pipeline" not in st.session_state:
            st.session_state[f"{subject}_{task}_pipeline"] = train_model(edfs)
        table = predict(st.session_state[f"{subject}_{task}_pipeline"], edfs)
        if table:
            correct = sum(table['equals'])
            total = len(table['equals'])
            accuracy = correct / total * 100
            tasks_accuracies[task].append(accuracy)
            st.toast(
                f"Subject: {subject} Task: {task} Accuracy: {accuracy:.2f}%",
                icon="✅",
            )
        for edf in edfs:
            edf.raw.close()
            edf.filtered.close()
    st.write(f"Task: {task} Accuracy: {sum(tasks_accuracies[task]) / len(tasks_accuracies[task]):.2f}%")

st.metric(
    label="Overall Accuracy",
    value=f"{sum([sum(tasks_accuracies[task]) / len(tasks_accuracies[task]) for task in tasks]) / len(tasks):.2f}%",
)
