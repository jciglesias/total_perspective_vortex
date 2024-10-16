import streamlit as st
import mne, os

def file_selector(folder_path='/mnt/nfs/homes/jiglesia/sgoinfre/files'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)
