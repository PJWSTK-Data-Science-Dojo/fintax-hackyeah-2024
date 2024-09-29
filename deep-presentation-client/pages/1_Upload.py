import time
import streamlit as st
from dotenv import load_dotenv

from utils.video import create_video
from utils.common import initialize

load_dotenv()

st.set_page_config(
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

def upload_video():
    if upload_video not in st.session_state:
        st.session_state.uploaded_video = None

    st.title("Przesyłanie filmu")

    uploaded_video = st.file_uploader("Prześlij film...", type=["mp4"])

    if uploaded_video:
        st.session_state.uploaded_video = uploaded_video

        with st.spinner("Przeysyłanie filmu..."):
            video_uuid = create_video(video_buffer=uploaded_video)

        st.session_state.video_uuid = video_uuid
        if not video_uuid:
            st.error("Napotkaliśmy problem z przesłaniem filmu!")
        else:
            st.info("""
Sukces!\n\n
Udało się przesłać twój film i rozpoczęła się analiza twojego filmu! Przejdź do zakładki Analiza, żeby poznać wyniki!\n
                    
Zostaniesz automatycznie przeniesiony za 10s.
            """)

            time.sleep(10)

            st.switch_page("pages/2_Analysis_Review.py")


if __name__ == "__main__":
    initialize("NoHome")
    upload_video()
