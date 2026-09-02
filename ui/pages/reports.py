"""
Weekly Wellness Report page.
"""

import streamlit as st

from utils.session import (
    is_logged_in,
)

from ui.navigation import (
    navigate,
)

from features.reports.services import (
    generate_weekly_report,
)


def show_reports_page():
    """
    Weekly wellness report.
    """

    if not is_logged_in():

        st.error(
            "Please login first."
        )

        return

    user_id = st.session_state.get(
        "user_id"
    )

    if not user_id:

        st.error(
            "User session not found."
        )

        return

    report = generate_weekly_report(
        user_id
    )

    st.title(
        "📋 Weekly Wellness Report"
    )

    st.caption(
        "Your AI-generated wellness summary."
    )

    st.divider()

    st.metric(
        "Wellness Score",
        f"{report['wellness_score']}/100"
    )

    st.success(
        f"Level: "
        f"{report['wellness_level']}"
    )

    st.divider()

    st.subheader(
        "🤖 AI Summary"
    )

    st.info(
        report["ai_summary"]
    )

    st.divider()

    st.subheader(
        "🧠 Memory Highlights"
    )

    if report[
        "memory_highlights"
    ]:

        for memory in report[
            "memory_highlights"
        ]:

            st.write(
                f"• {memory}"
            )

    else:

        st.write(
            "No memories yet."
        )

    st.divider()

    st.subheader(
        "🎯 Recommendations"
    )

    for recommendation in report[
        "recommendations"
    ]:

        st.write(
            f"✅ {recommendation}"
        )

    st.divider()

    if st.button(
        "← Back to Dashboard",
        use_container_width=True,
    ):

        navigate(
            "dashboard"
        )