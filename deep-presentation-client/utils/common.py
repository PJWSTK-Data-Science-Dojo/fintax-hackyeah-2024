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
            # page_title="ReviewAnalyzer",
            page_icon="🔬",
            # layout="wide",
            # initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("Analyzer"), unsafe_allow_html=True)
        # if "selected_text" not in st.session_state:
        #     st.session_state.selected_text = ""
        # if "search_wiki" not in st.session_state:
        #     st.session_state.search_wiki = False
    elif page == "DataExplorer":
        st.set_page_config(
            page_title="DataExplorer",
            page_icon="📖",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("DataExplorer"), unsafe_allow_html=True)


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
        # Use this to remove the empty space on top of the page
        # #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        #
        # Use this to remove "Deploy button (if header visibility is turned on"
        # .stDeployButton {{
        #         visibility: hidden;
        #     }}
        # This hids those stupid anchors ... but also removes pages from sidebar
        # /* Hide the link button https://discuss.streamlit.io/t/hide-titles-link/19783/13 */
        # .stApp a:first-child {{
        #     display: none;
        # }}
    elif page == "DataExplorer":
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
