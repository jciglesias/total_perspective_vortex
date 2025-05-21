import mne
import pywt
from mne.io import BaseRaw
from src.utils.utils import get_file_name
from src.Classes.edf import EDF
from src.utils.utils import read_raw_data, channels
import random

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

def load_data(subject: str, task: str):
    """
    Load and preprocess data from a list of files.
    """
    files = get_file_name(subject, task)
    edfs = []
    for file in files:
        edf = EDF(read_raw_data(f"../tpv_files/{subject}/{file}"))
        edf.filename = file
        edf.filtered = filter_data(edf.raw, 13, 30)
        edfs.append(edf)
    for_training = random.sample(range(len(edfs)), int(len(edfs) * 0.7))
    for i in range(len(edfs)):
        if i in for_training:
            edfs[i].training = True
        else:
            edfs[i].training = False
    return edfs

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

