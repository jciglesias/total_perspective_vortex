from src.data.Subject import Subject
import streamlit as st
from sklearn.pipeline import Pipeline
from src.treatment.reduction_algo import reduction_algo

if 'subject' not in st.session_state:
    st.write('No data loaded yet')
else:
    subject: Subject = st.session_state['subject']
    # • Dimensionality reduction algorithm (ie : PCA, ICA, CSP, CSSP...).
    features, labels = subject.treatment_pipeline()
    pipe: Pipeline = reduction_algo(2)
    pipe.fit(features, labels)
    st.write('Baseline runs')
    st.write(pipe.score(subject.baseline_runs.features, subject.baseline_runs.labels))
    # • Classification algorithm, there is plenty of choice among those available in sklearn,
    # to output the decision of what data chunk correspond to what kind of motion.
    # • "Playback" reading on the file to simulate a data stream.