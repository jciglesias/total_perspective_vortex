import mne
import matplotlib.pyplot as plt
from mne.io import BaseRaw
import numpy as np
import streamlit as st

subjects = [f"S{n:03}" for n in range(1, 110)]

tasks = {
    'open and close fist': ["R03", "R07", "R11"],
    'imagine opening and closing fist': ["R04", "R08", "R12"],
    'open and close fists or feets': ["R05", "R09", "R13"],
    'imagine opening and closing fists or feets': ["R06", "R10", "R14"],
}

channels = [
    'Cp3.',
    'C3..',
    'Fc4.',
    'Cpz.',
    'Cp4.',
    'Fc3.',
    'Fcz.',
    'Cz..',
    'C4..',
    ]

cross_val_column_config = {
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
        }

def get_file_name(subject, task):
    """
    Get the file name based on the subject and task.
    """
    if subject not in subjects:
        raise ValueError(f"Invalid subject: {subject}")
    if task not in tasks:
        raise ValueError(f"Invalid task: {task}")
    
    files = [f'{subject}{task_}.edf' for task_ in tasks[task]]
    return files

def read_raw_data(filename: str):
    """
    Read raw data from a file and return the raw object.
    """
    try:
        raw = mne.io.read_raw_edf(filename, preload=True)
        return raw
    except Exception as e:
        print(f"Error reading raw data: {e}")
        return None

def create_image(raw: BaseRaw, filename: str):
    fig = raw.plot()
    file_address = f"./images/{filename}"
    fig.savefig(file_address, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return file_address

def get_epochs_and_labels(raw: BaseRaw):
    """
    Get epochs and labels from the raw data.
    """
    try:
        events, events_id = mne.events_from_annotations(raw)
        epochs = mne.Epochs(raw, events, events_id, tmin=0, tmax=1, baseline=None, picks=channels)
        labels = epochs.events[:, -1]
        return epochs, labels
    except Exception as e:
        print(f"Error getting epochs and labels: {e}")
        return None, None

def extract_features(epoch_data):
    # epoch_data shape: (n_channels, n_times)
    # features: mean, std, band power per channel
    features = []
    for ch in epoch_data:
        features.append(np.mean(ch))
        features.append(np.std(ch))
        features.append(np.sum(ch ** 2))
    return features
