import streamlit as st

from ui.navigation import navigate


def show_landing_page():
    """Display the MindEase landing page."""

    st.markdown(
        """
        <div style="text-align:center; padding-top:20px;">
            <h1>🌸 MindEase</h1>
            <h3>Your AI Mental Wellness Companion</h3>
            <p style="font-size:18px;">
                Talk. Reflect. Heal. Grow — One day at a time.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🤖 **AI Chat**\n\nTalk with a compassionate AI companion.")
        st.info("📖 **Journal**\n\nCapture your daily thoughts.")

    with col2:
        st.info("😊 **Mood Tracker**\n\nMonitor your emotional wellbeing.")
        st.info("📊 **Insights**\n\nView your wellness progress.")

    st.divider()

    st.success(
        '🌿 **Quote of the Day**\n\n'
        '"Small steps every day lead to big changes."'
    )

    st.write("")
    st.write("")

    if st.button("🚀 Get Started", use_container_width=True):
        navigate("signup")

    st.write("")

    col_left, col_mid, col_right = st.columns([2, 2, 2])

    with col_mid:
        if st.button("Already have an account? Login"):
            navigate("login")