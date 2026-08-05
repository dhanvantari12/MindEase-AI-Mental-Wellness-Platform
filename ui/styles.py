import streamlit as st


def load_css(theme):
    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color: {theme["background"]};
        }}

        .main-title {{
            text-align:center;
            font-size:42px;
            font-weight:700;
            color:{theme["primary"]};
            margin-top:20px;
        }}

        .subtitle {{
            text-align:center;
            font-size:18px;
            color:{theme["secondary_text"]};
            margin-bottom:30px;
        }}

        .card {{
            background:{theme["card"]};
            padding:35px;
            border-radius:20px;
            box-shadow:0px 8px 20px rgba(0,0,0,0.08);
        }}

        div.stButton > button {{
            width:100%;
            border-radius:15px;
            height:48px;
            font-size:16px;
            font-weight:bold;
            background:{theme["primary"]};
            color:white;
            border:none;
        }}

        div.stButton > button:hover {{
            transform:scale(1.02);
            transition:0.2s;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )