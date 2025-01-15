import mne
from src.data.EEG_dir import annotation_codes, experimental_runs

def filter_raw_data(raw: mne.io.Raw, low_freq: int, high_freq: int) -> mne.io.Raw:
    raw.filter(low_freq, high_freq, fir_design='firwin')
    return raw

class Subject:

    def __init__(self, subject_id: int):
        self.subject_id = subject_id
        self.lr_runs = []
        self.both_runs = []
        self.baseline_runs = []
        self.eeg = None
        self.annotations = None
        self.events = None
        self.epochs = None
    
    def load_data(self, filename: str):
        run_number = filename.split('R')[-1].split('.')[0]
        run = mne.io.read_raw_edf(filename, preload=True)
        # run = filter_raw_data(run, 0.5, 161)
        if run_number in annotation_codes['LR']['runs']:
            self.lr_runs.append(run)
        elif run_number in annotation_codes['both']['runs']:
            self.both_runs.append(run)
        elif run_number in experimental_runs['baseline']:
            self.baseline_runs.append(run)
        else:
            print(f'Run number {run_number} not found in the experimental runs')
