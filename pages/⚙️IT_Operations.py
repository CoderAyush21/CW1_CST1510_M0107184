import streamlit as st

st.set_page_config(
    page_title="IT Operations",
    layout="wide",
)

st.title("IT OPERATIONS DASHBOARD")

if st.session_state.get("logged_in") != True:
    st.error("Please Log in")
    st.stop()