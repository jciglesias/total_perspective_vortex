import streamlit as st
import mne, os, plotly.express as px
from scipy import signal
from src.data.Subject import Subject


folder_path=f'{os.environ["HOME"]}/Documents/tpv_files'
filenames = os.listdir(folder_path)
folders = [f for f in filenames if f.startswith('S')]
folders.sort()
folder = folders[0]
subject = Subject(int(folder[1:]))
filenames = [f for f in os.listdir(f"{folder_path}/{folder}") if f.endswith('.edf')]
left_col, right_col = st.columns(2)
left_col.write('Raw Data')
right_col.write('Filtered Data')
for filename in filenames:
    subject.load_data(f"{folder_path}/{folder}/{filename}", left_col, right_col)
st.session_state['subject'] = subject
st.dialog('Data loaded successfully')
