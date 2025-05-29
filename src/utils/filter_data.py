import mne
import pywt
from src.utils.utils import get_file_name, channels
from src.Classes.edf import EDF
from src.utils.utils import read_raw_data, get_epochs_and_labels
from sklearn.model_selection import train_test_split


def filter_data(raw: mne.io.BaseRaw, l_freq, h_freq):
    """
    Filter the raw data using a bandpass filter.
    """
    try:
        raw.filter(l_freq, h_freq, fir_design='firwin')
        wavelet = 'db4'
        coeffs = pywt.swt(raw.get_data(), wavelet, level=1)
        detail_coeffs = coeffs[0][1]
        annotations = raw.annotations
        raw = mne.io.RawArray(detail_coeffs, raw.info, first_samp=raw.first_samp)
        raw.set_annotations(annotations)
        return raw
    except Exception as e:
        print(f"Error filtering data: {e}")
        return None

def load_data(subject: str, task: str, folder: str = "tpv_files"):
    """
    Load and preprocess data from a list of files.
    """
    files = get_file_name(subject, task)
    edfs = []
    for file in files:
        edf = EDF(read_raw_data(f"../{folder}/{subject}/{file}"))
        edf.filename = file
        edf.filtered = filter_data(edf.raw, 0, 30)
        edf.epochs, edf.labels = get_epochs_and_labels(edf.raw)
        edf.x_train, edf.x_test, edf.y_train, edf.y_test = train_test_split(edf.epochs.get_data(), edf.labels, test_size=0.3, random_state=42)
        # edf.x_train, edf.x_test, edf.y_train, edf.y_test = train_test_split(edf.epochs.get_data(picks=channels), edf.labels, test_size=0.3, random_state=42)
        edfs.append(edf)
    return edfs
