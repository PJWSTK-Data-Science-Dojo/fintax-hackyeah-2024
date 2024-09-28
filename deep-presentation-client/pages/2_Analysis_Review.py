import streamlit as st

def audio_review():
    pass

def video_review():
    pass

def text_review():
    pass


def analysis_review():
    st.title("Analysis Review")

    video_tab, audio_tab, text_tab = st.tabs(["Video", "Audio", "Text"])

    with video_tab:
        video_review()
    
    with audio_tab:
        audio_review()

    with text_tab:
        text_review()

    

if __name__ == "__main__":
    analysis_review()
