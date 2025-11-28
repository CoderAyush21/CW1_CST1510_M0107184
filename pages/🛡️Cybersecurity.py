import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents
st.set_page_config(
    page_title="Cybersecurity",
    layout="wide",
)

st.title("CYBERSECURITY INTELLIGENCE DASHBOARD")


if st.session_state.get("logged_in") != True:
    st.error("Please Log in")
    st.stop()

# Display Cyber Incidents Data

df_incidents = get_all_incidents()

# Display Cyber Incidents Bar Chart by Severity
st.subheader("Cyber Incidents by Severity")

severity_counts = df_incidents["severity"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]

st.bar_chart(severity_counts.set_index("severity"))