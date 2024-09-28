import streamlit as st



def upload_viideo():
    st.title("Upload Video")

    uploaded_video = st.file_uploader("Or choose a video...", type=["mp4"], key="uploaded_video")


if __name__ == "__main__":
    upload_viideo() 