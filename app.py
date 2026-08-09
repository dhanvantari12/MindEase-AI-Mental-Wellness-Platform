import streamlit as st
from ui.pages.mood import show_mood_page
from ui.navigation import initialize_navigation
from ui.pages.journal import show_journal_page

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

elif st.session_state.page == "mood":
    show_mood_page()
    
elif st.session_state.page == "journal":
    show_journal_page()