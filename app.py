import streamlit as st

from ui.navigation import initialize_navigation


st.set_page_config(
    page_title="MindEase",
    page_icon="🌸",
    layout="wide",
)

initialize_navigation()

from ui.pages.landing import show_landing_page
from ui.pages.login import show_login_page
from ui.pages.signup import show_signup_page
from ui.pages.dashboard import show_dashboard

if st.session_state.page == "landing":
    show_landing_page()

elif st.session_state.page == "login":
    show_login_page()

elif st.session_state.page == "signup":
    show_signup_page()

elif st.session_state.page == "dashboard":
    show_dashboard()