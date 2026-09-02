import streamlit as st

from ui.navigation import initialize_navigation, navigate

st.set_page_config(page_title="Navigation Test")

initialize_navigation()

st.write("Current page:", st.session_state.page)

if st.button("Open Safe Space"):
    navigate("safe_space")

st.write("After navigation:", st.session_state.page)