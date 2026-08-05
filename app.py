import streamlit as st

from ui.navigation import initialize_navigation

st.set_page_config(
    page_title="MindEase",
    page_icon="🌸",
    layout="wide",
)

initialize_navigation()

st.title("MindEase 🌸")

st.write(f"Current Page: **{st.session_state.page}**")