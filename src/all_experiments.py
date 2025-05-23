from src.Classes.model import Model
from src.utils.filter_data import load_data
from src.utils.predict import predict
from src.utils.train_model import train_model
from src.utils.utils import tasks, subjects
import streamlit as st

tasks_accuracies = {}
st.write("Mean accuracy of the four different experiments for all 109 subjects:")
with st.spinner("Loading data...", show_time=True):
    for task in tasks:
        tasks_accuracies[task] = []
        for subject in subjects:
            model = Model(load_data(subject, task))
            train_model(model)
            table = predict(model)
            if table:
                correct = sum(table['equals'])
                total = len(table['equals'])
                accuracy = correct / total * 100
                tasks_accuracies[task].append(accuracy)
                st.toast(
                    f"Subject: {subject} Task: {task} Accuracy: {accuracy:.2f}%",
                    icon="✅",
                )
            for edf in model.edfs:
                edf.raw.close()
                edf.filtered.close()
        st.write(f"Experiment: {task} Accuracy = {sum(tasks_accuracies[task]) / len(tasks_accuracies[task]):.2f}%")

st.metric(
    label="Overall Accuracy",
    value=f"{sum([sum(tasks_accuracies[task]) / len(tasks_accuracies[task]) for task in tasks]) / len(tasks):.2f}%",
)
