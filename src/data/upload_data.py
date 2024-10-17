import streamlit as st
import mne, os, plotly.express as px
from scipy import signal

def file_selector(folder_path='/mnt/nfs/homes/jiglesia/sgoinfre/files') -> str:
    filenames = os.listdir(folder_path)
    folders = [f for f in filenames if f.startswith('S')]
    folders.sort()
    selected_folder = st.selectbox('Select a folder', folders, index=None, placeholder='Select a folder')
    if selected_folder is not None:
        filenames = [f for f in os.listdir(os.path.join(folder_path, selected_folder)) if f.endswith('.edf')]
        filenames.sort()
    selected_filename = st.selectbox('Select a file', filenames, index=None, placeholder='Select a file', disabled=selected_folder is None)
    return f"{folder_path}/{selected_folder}/{selected_filename}"

filename = file_selector()
tab1, tab2 = st.tabs(['Raw', 'Filtered'])
if filename.endswith('.edf'):
    tab1.write('You selected `%s`' % filename)
    raw = mne.io.read_raw_edf(filename)
    fig = raw.plot()
    tab1.pyplot(fig)
    # obtain signal's specter
    sig = signal.cwt(raw.get_data()[0], signal.ricker, widths=range(1, 31))
    fig2 = px.imshow(sig, aspect='auto')
    # fig2 = raw.compute_psd(fmax=50).plot(picks='data', exclude='bads')
    tab2.plotly_chart(fig2)