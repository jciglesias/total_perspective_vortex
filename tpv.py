import streamlit as st

home_page = st.Page("src/home.py", title="Home", icon=":material/home:")

subject_page = st.Page("src/by_subject.py", title="By Subject", icon=":material/cloud_upload:")

experiments_page = st.Page("src/all_experiments.py", title="All Experiments", icon=":material/insert_chart:")

st.set_page_config(page_title="Total Perspective Vortex", page_icon=":material/storm:", layout="wide")
pg = st.navigation(
    [home_page, subject_page, experiments_page],
)
pg.run()