import streamlit as st

home_page = st.Page("src/home.py", title="Home", icon=":material/home:")

upload_page = st.Page("src/data/upload_data.py", title="Upload Data", icon=":material/cloud_upload:")
# parse_page = st.Page("src/data/parsing.py", title="Parse Data", icon=":material/settings:")
# preprocesing_page = st.Page("src/data/preprocessing.py", title="Preprocessing", icon=":material/transform:")
# formatting_page = st.Page("src/data/formatting.py", title="Formatting", icon=":material/format_align_left:")

implement_page = st.Page("src/implementation/implement.py", title="Implement Model", icon=":material/insert_chart:")

model_page = st.Page("src/model/model.py", title="Model", icon=":material/insert_chart:")

pipeline_page = st.Page("src/treatment/pipeline.py", title="Pipeline", icon=":material/insert_chart:")

st.set_page_config(page_title="Total Perspective Vortex", page_icon=":material/storm:")
pg = st.navigation({
    "home": [home_page],
    "data": [upload_page],
    "treatment": [pipeline_page],
    "implementation": [implement_page],
    "model": [model_page],
    })
pg.run()