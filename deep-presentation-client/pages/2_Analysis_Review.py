import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from utils import api

load_dotenv()

API_URL = os.getenv('API_URL')
VIDEO_STORAGE = os.getenv('VIDEO_STORAGE')

EMOTICON_MAP = {
    'angry': ('😡', '#FF6B6B'),
    'disgust': ('🤢', '#9ACD32'),
    'fear': ('😨', '#004976'),
    'happy': ('😃', '#F4D03F'),
    'sad': ('😢', '#5B9BD5'),
    'surprise': ('😮', '#FFB6C1'),
    'neutral': ('😐', '#C0C0C0'),
    None: ('😐', '#E0E0E0')
}

def mock_analysis_response():
    return {
        'frames': [
            {'start': 0, 'end': 1, 'emotion': None},
            {'start': 1, 'end': 2, 'emotion': None},
            {'start': 2, 'end': 3, 'emotion': None},
            {'start': 3, 'end': 4, 'emotion': None},
            {'start': 4, 'end': 5, 'emotion': None},
            {'start': 5, 'end': 6, 'emotion': None},
            {'start': 6, 'end': 7, 'emotion': None},
            {'start': 7, 'end': 8, 'emotion': None},
            {'start': 8, 'end': 9, 'emotion': None},
            {'start': 9, 'end': 10, 'emotion': None},
            {'start': 10, 'end': 11, 'emotion': None},
            {'start': 11, 'end': 12, 'emotion': 'angry'},
            {'start': 12, 'end': 13, 'emotion': 'sad'},
            {'start': 13, 'end': 14, 'emotion': 'sad'},
            {'start': 14, 'end': 15, 'emotion': 'sad'},
            {'start': 15, 'end': 16, 'emotion': 'angry'},
            {'start': 16, 'end': 17, 'emotion': 'sad'},
            {'start': 17, 'end': 18, 'emotion': 'angry'},
            {'start': 18, 'end': 19, 'emotion': 'sad'},
            {'start': 19, 'end': 20, 'emotion': 'sad'},
            {'start': 20, 'end': 21, 'emotion': 'sad'},
            {'start': 21, 'end': 22, 'emotion': 'angry'},
            {'start': 22, 'end': 23, 'emotion': 'angry'},
            {'start': 23, 'end': 24, 'emotion': 'angry'},
            {'start': 24, 'end': 25, 'emotion': 'sad'},
            {'start': 25, 'end': 26, 'emotion': 'angry'},
            {'start': 26, 'end': 27, 'emotion': 'sad'},
            {'start': 27, 'end': 28, 'emotion': 'sad'},
            {'start': 28, 'end': 29, 'emotion': 'angry'},
            {'start': 29, 'end': 30, 'emotion': 'angry'},
            {'start': 30, 'end': 31, 'emotion': 'angry'},
            {'start': 31, 'end': 32, 'emotion': 'neutral'}
        ]
    }


@st.cache_data
def cached_analysis_response():
    return mock_analysis_response()


def render_emotions_and_legend(video_col):
    with video_col:
        response = cached_analysis_response()
        frames = response['frames']
        color_list = [EMOTICON_MAP[frame['emotion']][1] for frame in frames]

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
            for emotion, (emoticon, color) in EMOTICON_MAP.items():
                if emotion is None:
                    continue
                legend_html += (
                    f'<div style="background-color: {color}; padding: 10px 15px; border-radius: 5px; display: flex; align-items: center; '
                    f'justify-content: center; height: 50px; min-width: 100px; margin: 5px; color: black">'
                    f'{emoticon} - {emotion.capitalize()}'
                    '</div>'
                )
            legend_html += '</div>'
            st.markdown(legend_html, unsafe_allow_html=True)


def video_review():
    video_col = st.columns(1)[0]
    render_emotions_and_legend(video_col)


def audio_review():
    video_uuid = "0000-4444-0000-4444"
    data = api.fetch_audio_analysis(video_uuid)


def text_review():
    video_uuid = "0000-4444-0000-4444"
    data = api.fetch_full_analysis(video_uuid)


def analysis_review():
    st.set_page_config(layout="wide")

    st.title("Analysis Review")

    if "video_uuid" not in st.session_state or not st.session_state.video_uuid:
        st.switch_page("pages/1_Upload.py")

    subtitles = api.fetch_subtitles(st.session_state.video_uuid)
    subtitles_path = Path()
    print(subtitles_path)
    print(subtitles_path.exists())
    st.video(st.session_state.uploaded_video, subtitles={
        "Polish": f"{VIDEO_STORAGE }/{st.session_state.video_uuid}/{st.session_state.video_uuid}.srt"
        })

    video_tab, audio_tab, text_tab = st.tabs(["Video", "Mowa", "Pełna analiza"])

    with video_tab:
        video_review()

    with audio_tab:
        audio_review()

    with text_tab:
        text_review()


if __name__ == "__main__":
    analysis_review()
