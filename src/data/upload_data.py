import streamlit as st
import mne, os, plotly.express as px
from scipy import signal
from src.data.Subject import Subject, filter_raw_data


def file_selector(folder_path=f'{os.environ["HOME"]}/Documents/tpv_files') -> list:
    filenames = os.listdir(folder_path)
    folders = [f for f in filenames if f.startswith('S')]
    folders.sort()
    subjects = []
    # for folder in folders:
    folder = folders[0]
    subject = Subject(int(folder[1:]))
    filenames = [f for f in os.listdir(f"{folder_path}/{folder}") if f.endswith('.edf')]
    for filename in filenames:
        subject.load_data(f"{folder_path}/{folder}/{filename}")
    subjects.append(subject)
    return subjects
    # selected_folder = st.selectbox('Select a folder', folders, index=None, placeholder='Select a folder')
    # if selected_folder is not None:
    #     filenames = [f for f in os.listdir(f"{folder_path}/{selected_folder}") if f.endswith('.edf')]
    #     filenames.sort()
    # selected_filename = st.selectbox('Select a file', filenames, index=None, placeholder='Select a file', disabled=selected_folder is None)
    # return f"{folder_path}/{selected_folder}/{selected_filename}"


subject = file_selector()
left_col, right_col = st.columns(2)
left_col.write('Raw Data')
right_col.write('Filtered Data')
for run in subject[0].lr_runs:
    fig = run.plot()
    left_col.pyplot(fig)
    filtered_fig = filter_raw_data(run, 1, 50).plot()
    right_col.pyplot(filtered_fig)

# st.write(subject[0].lr_runs)
# try :
#     filename = file_selector()
# except Exception as e :
#     st.write('No file selected')
#     filename = ''
# tab1, tab2, tab, tab3 = st.tabs(['Raw', 'Filtered', 'Raw Data', 'ICA'])
# if filename.endswith('.edf'):
#     # tab1.write('You selected `%s`' % filename)
#     raw = mne.io.read_raw_edf(filename, preload=True)
#     tab.write(raw.info)
#     fig = raw.plot()
#     tab1.pyplot(fig)
    # obtain signal's specter
    # sig = signal.cwt(raw.get_data()[0], signal.ricker, widths=range(1, 31))
    # fig2 = px.imshow(sig, aspect='auto')
    # fig2 = raw.compute_psd(fmax=50).plot(picks='data', exclude='bads')
    # tab2.plotly_chart(fig2)
    # ica = mne.preprocessing.ICA(n_components=64, random_state=97, max_iter=800)
    # ica.fit(raw)
    # tab3.write(ica)
    # fig3 = ica.plot_properties(raw)
    # tab3.pyplot(fig3)