import streamlit as st
import base64


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def initialize(page: str) -> None:
    if page == "Home":
        st.set_page_config(
            page_icon="🔬",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("Analyzer"), unsafe_allow_html=True)
    elif page == "NoHome":
        st.markdown(get_page_bg_data("NoHome"), unsafe_allow_html=True)


def get_page_bg_data(page: str) -> str:
    if page == "Analyzer":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/main_dark_bg.jpg")}");
            background-position: 45% 0%;
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
    elif page == "NoHome":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}
        </style>
        """
    return ""
