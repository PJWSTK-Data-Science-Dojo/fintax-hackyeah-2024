import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from utils import api

load_dotenv()

API_URL = os.getenv('API_URL')
VIDEO_STORAGE = os.getenv('VIDEO_STORAGE')

EMOTICON_MAP = {
    'angry': ('😡', '#FF6B6B', 'Złość'),
    'disgust': ('🤢', '#9ACD32', 'Obrzydzenie'),
    'fear': ('😨', '#004976', 'Strach'),
    'happy': ('😃', '#F4D03F', 'Radość'),
    'sad': ('😢', '#5B9BD5', 'Smutek'),
    'surprise': ('😮', '#FFB6C1', 'Zaskoczenie'),
    'neutral': ('😐', '#C0C0C0', 'Neutralny'),
    None: ('😐', '#C0C0C0', 'Neutralny')
}


def render_emotions_and_legend(video_col, emotions_frames):
    with video_col:
        color_list = [EMOTICON_MAP[frame['emotion']][1] for frame in emotions_frames]

        # Render the emotion color bar
        bar_container = st.container()
        with bar_container:
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            color_bar_html = '<div style="display: flex; justify-content: center; align-items: center; width: 100%;">'
            for color in color_list:
                color_bar_html += f'<div style="flex: 1; height: 50px; background-color: {color};"></div>'
            color_bar_html += '</div>'
            st.markdown(color_bar_html, unsafe_allow_html=True)

        # Render the legend
        legend_container = st.container()
        with legend_container:
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)  # Add some margin
            legend_html = '<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; width: 100%;">'  # Set the fixed width to match the video
            for emotion, (emoticon, color, polish_emotion) in EMOTICON_MAP.items():
                if emotion is None:
                    continue
                legend_html += (
                    f'<div style="background-color: {color}; padding: 10px 15px; border-radius: 5px; display: flex; align-items: center; '
                    f'justify-content: center; height: 50px; min-width: 100px; margin: 5px; color: black">'
                    f'{emoticon} - {polish_emotion.capitalize()}'
                    '</div>'
                )
            legend_html += '</div>'
            st.markdown(legend_html, unsafe_allow_html=True)


def render_textual_analysis(video_col, textual_report):
    with video_col:
        st.markdown("### Raport analizy tekstowej")

        # AI Advice
        st.markdown("**Porady AI:**")
        st.markdown(textual_report.get('ai_advice', 'Brak porad AI.'))

        # Flags
        st.markdown("Znalezione błędy:")
        st.checkbox("Użyto zbyt wielu liczb", value=textual_report.get('too_many_numbers_usesd', False), disabled=True)
        st.checkbox("Wykryto zmianę tematu", value=textual_report.get('chage_of_topic', False), disabled=True)
        st.checkbox("Wykryto powtórzenia", value=textual_report.get('repetitions', False), disabled=True)
        st.checkbox("Użyto strony biernej", value=textual_report.get('passive_voice', False), disabled=True)

        # Further Questions
        st.markdown("**Dalsze pytania do rozważenia:**")
        st.markdown(textual_report.get('further_questions', 'Brak pytań.'))

        # Target Audience
        st.markdown(f"**Grupa docelowa:** {textual_report.get('target_audienc', 'Nie określono')}")


def video_review(video_analysis):
    video_col = st.columns(1)[0]
    render_emotions_and_legend(video_col, video_analysis['video']['emotions_report']['frames'])

    render_textual_analysis(video_col, video_analysis['video']['textual_report'])


def audio_review():
    video_uuid = "0000-4444-0000-4444"
    data = api.fetch_analysis_data(video_uuid)


def text_review():
    video_uuid = "0000-4444-0000-4444"
    data = api.fetch_full_analysis(video_uuid)


def analysis_review():
    st.set_page_config(layout="wide")

    st.title("Analiza filmu")

    if "video_uuid" not in st.session_state or not st.session_state.video_uuid:
        st.switch_page("pages/1_Upload.py")

    with st.spinner("Analiza w toku..."):
        while True:
            stage_response = api.fetch_analysis_stage(st.session_state.video_uuid)
            stages = stage_response.get("stages", [])
            if any(stage.get("stage") == "done_visual" for stage in stages):
                break
            time.sleep(1)

    video_analysis = api.fetch_video_analysis_data(st.session_state.video_uuid)

    subtitles = api.fetch_subtitles(st.session_state.video_uuid)
    subtitles_path = Path()
    print(subtitles_path)
    print(subtitles_path.exists())
    st.video(st.session_state.uploaded_video, subtitles={
        "Polish": f"{VIDEO_STORAGE}/{st.session_state.video_uuid}/{st.session_state.video_uuid}.srt"
    })

    video_tab, audio_tab, text_tab = st.tabs(["Video", "Mowa", "Pełna analiza"])

    with video_tab:
        video_review(video_analysis)

    with audio_tab:
        audio_review()

    with text_tab:
        text_review()


if __name__ == "__main__":
    analysis_review()
