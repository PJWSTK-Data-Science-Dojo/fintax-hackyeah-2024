import time
import streamlit as st
from dotenv import load_dotenv

from utils.video import create_video
load_dotenv()


def upload_video():
    st.title("Przesyłanie filmu")

    uploaded_video = st.file_uploader("Prześlij film...", type=["mp4"], key="uploaded_video")
    
    if uploaded_video:
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
    upload_video() 