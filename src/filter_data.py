import mne
import pywt
import streamlit as st
from src.utils import get_file_name

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

def filter_data(raw: mne.io.BaseRaw, l_freq, h_freq):
    """
    Filter the raw data using a bandpass filter.
    """
    try:
        raw.filter(l_freq, h_freq, fir_design='firwin')
        wavelet = 'db4'
        aprox_coeffs, detail_coeffs = pywt.dwt(raw.get_data(), wavelet, mode='symmetric')
        annotations = raw.annotations
        raw = mne.io.RawArray(detail_coeffs, raw.info, first_samp=raw.first_samp)
        raw.set_annotations(annotations)
        return raw
    except Exception as e:
        print(f"Error filtering data: {e}")
        return None

def formating_data(raw: mne.io.BaseRaw):
    """
    Format the data for further processing.
    """
    try:
        events, events_id = mne.events_from_annotations(raw)
        epochs = mne.Epochs(raw, events, events_id, tmin=0, tmax=1, baseline=None)
        return epochs
    except Exception as e:
        print(f"Error formatting data: {e}")
        return None

def preprocess_data(filename: str):
    """
    Preprocess the data by reading, filtering, and formatting it.
    """
    raw = read_raw_data(filename)
    if raw is None:
        return None

    filtered_raw = filter_data(raw, 13, 30)
    if filtered_raw is None:
        return None

    epochs = formating_data(filtered_raw)
    if epochs is None:
        return None

    return epochs

def load_data(subject: str, task: str):
    """
    Load and preprocess data from a list of files.
    """
    files = get_file_name(subject, task)
    st.session_state[f"{subject}_{task}_raws"] = []
    st.session_state[f"{subject}_{task}_filtered_raws"] = []
    filtered_raws = st.session_state[f"{subject}_{task}_filtered_raws"]
    for file in files:
        raw = read_raw_data(f"../tpv_files/{subject}/{file}")
        st.session_state[f"{subject}_{task}_raws"].append(raw)
        filtered_raw = filter_data(raw, 13, 30)
        filtered_raws.append(filtered_raw)
    st.toast("Data loaded successfully!")
