import streamlit as st

st.set_page_config(
    page_title="Data Science",
    layout="wide",
)

st.title("DATA SCIENCE ANALYTICS DASHBOARD")

if st.session_state.get("logged_in") != True:
    st.error("Please Log in")
    st.stop()