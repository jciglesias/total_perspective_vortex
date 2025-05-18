import mne
import pywt
from mne.io import BaseRaw
import streamlit as st
from src.utils.utils import get_file_name
from src.Classes.edf import EDF
from src.utils.utils import read_raw_data

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

def create_image(raw: BaseRaw, filename: str):
    fig = raw.plot()
    file_address = f"./images/{filename}"
    fig.savefig(file_address, format="png", dpi=300, bbox_inches="tight")
    return file_address

@st.cache_data(show_spinner=True, persist=True)
def load_data(subject: str, task: str):
    """
    Load and preprocess data from a list of files.
    """
    files = get_file_name(subject, task)
    edfs = []
    for file in files:
        edf = EDF(read_raw_data(f"../tpv_files/{subject}/{file}"))
        edf.raw_image = create_image(edf.raw, f"{file}_raw_image.png")
        edf.filtered = filter_data(edf.raw, 13, 30)
        edf.filtered_image = create_image(edf.filtered, f"{file}_filtered_image.png")
        edfs.append(edf)
    return edfs

def get_epochs_and_labels(raw: BaseRaw):
    """
    Get epochs and labels from the raw data.
    """
    try:
        events, events_id = mne.events_from_annotations(raw)
        epochs = mne.Epochs(raw, events, events_id, tmin=0, tmax=1, baseline=None)
        labels = epochs.events[:, -1]
        return epochs, labels
    except Exception as e:
        print(f"Error getting epochs and labels: {e}")
        return None, None

