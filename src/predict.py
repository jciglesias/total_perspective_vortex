import streamlit as st

def predict(pipeline, raws):
    """
    Predict the labels for the given raw data using the trained pipeline.
    """
    st.toast("Predicting...")
    for raw in raws:
        # predictions = pipeline.predict(raw)
        # st.write(predictions)
        st.pyplot(raw.plot())
    st.toast("Prediction completed!")