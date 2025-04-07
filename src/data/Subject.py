import mne
from mne.io import BaseRaw
from src.data.EEG_dir import annotation_codes, experimental_runs
import streamlit as st
import pywt
import numpy as np

class Runs:

    filtered_runs = []
    features = []
    labels = []
    
    def __init__(self, experiment: str):
        self.experiment = experiment

    # @staticmethod
    # def get_labels(run: BaseRaw):
    #     annotations = run.annotations
    #     labels = [str(x['description']) for x in annotations]
    #     return labels

    @staticmethod
    def filter_wavelet_transform(raw: mne.io.Raw, low_freq: int, high_freq: int) -> mne.io.Raw:
        raw.filter(low_freq, high_freq, fir_design='firwin')
        wavelet = 'db4'
        
        data, detail_coeffs = pywt.dwt(raw.get_data(), wavelet)
        annotations = raw.annotations
        raw = mne.io.RawArray(data, raw.info, first_samp=raw.first_samp)
        raw.set_annotations(annotations)
        return raw, detail_coeffs

    def add_run(
            self,
            run: BaseRaw,
            raw_plots, 
            filtered_plots
            ):
        raw_plots.pyplot(run.plot())
        run, detail_coeffs = self.filter_wavelet_transform(run, 13, 30) # Filter betha waves
        filtered_plots.pyplot(run.plot())
        self.filtered_runs.append(run)

        flattened_coeffs = np.ravel(detail_coeffs)
        self.features.append(flattened_coeffs)
        # self.labels = self.get_labels(run)
    
    def dimension_reduction(self):
        if len(self.filtered_runs) > 0:
            for run in self.filtered_runs:
                events, events_id = mne.events_from_annotations(run)
                epochs = mne.Epochs(run, events, events_id, tmin=0, tmax=1, baseline=None)
                epochs.plot_psd()
                self.labels.append(epochs.events[:, -1])
                self.features.append(epochs.get_data())
                picks = mne.pick_types(epochs.info, eeg=True, eog=False)
                self.features.append(epochs.get_data()[:, picks])

        else:
            print('No runs to process')

class Subject:

    def __init__(self, subject_id: int):
        self.subject_id = subject_id
        self.lr_runs = Runs('LR')
        self.both_runs = Runs('both')
        self.baseline_runs = Runs('baseline')
        self.eeg = None
        self.annotations = None
        self.events = None
        self.epochs = None
    
    def load_data(self, filename: str, raw_plots, filtered_plots):
        run_number = filename.split('R')[-1].split('.')[0]
        run = mne.io.read_raw_edf(filename, preload=True)
        if run_number in annotation_codes['LR']['runs']:
            self.lr_runs.add_run(run, raw_plots, filtered_plots)
        elif run_number in annotation_codes['both']['runs']:
            self.both_runs.add_run(run, raw_plots, filtered_plots)
        elif run_number in experimental_runs['baseline']:
            self.baseline_runs.add_run(run, raw_plots, filtered_plots)
        else:
            print(f'Run number {run_number} not found in the experimental runs')
    
    def treatment_pipeline(self):
        self.lr_runs.dimension_reduction()
        self.both_runs.dimension_reduction()
        self.baseline_runs.dimension_reduction()
        self.features = self.lr_runs.features + self.both_runs.features + self.baseline_runs.features
        self.labels = self.lr_runs.labels + self.both_runs.labels + self.baseline_runs.labels
        return self.features, self.labels
