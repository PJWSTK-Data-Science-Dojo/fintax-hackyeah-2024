import os

import streamlit as st
from dotenv import load_dotenv
from streamlit_player import st_player

load_dotenv('.env.local')

API_URL = os.getenv('API_URL')
VIDEO_STORAGE = os.getenv('VIDEO_STORAGE')

# for emotion, (emoticon, color) in EMOTICON_MAP.items():
EMOTICON_MAP = {
    'angry': ('😡', '#FF5733'),
    'disgust': ('🤢', '#8DFF33'),
    'fear': ('😨', '#33FFF5'),
    'happy': ('😃', '#FFE333'),
    'sad': ('😢', '#335BFF'),
    'surprise': ('😮', '#FF33EC'),
    'neutral': ('😐', '#A6A6A6'),
    None: ('😐', '#A6A6A6')
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


# def st_player_with_timestamp(url, height=None, progress_interval=1000):
#     timestamp_placeholder = st.empty()
#
#     options = {
#         "events": ["onProgress"],
#         "progress_interval": progress_interval,
#         "height": height
#     }
#
#     event = st_player(url, **options)
#     response = cached_analysis_response()
#
#     if event and isinstance(event, tuple) and len(event) > 1 and event[0] == 'onProgress':
#         current_time = int(event[1].get('playedSeconds', 0))
#         timestamp_placeholder.text(f"Aktualna emocja: {get_emotion_from_timestamp(response, current_time)}")
#

def video_review():
    if 'CURRENT_VIDEO_UUID' not in st.session_state:
        st.write("No video selected for review.")
        return

    video_col, legend_col = st.columns([4, 1])

    with video_col:
        st_player("https://youtu.be/CmSKVW1v0xM")

        response = cached_analysis_response()
        frames = response['frames']
        color_list = [EMOTICON_MAP[frame['emotion']][1] for frame in frames]

        color_bar_html = '<div style="display: flex; width: 100%; height: 30px; margin-top: 10px;">'
        for color in color_list:
            color_bar_html += f'<div style="flex: 1; background-color: {color};"></div>'
        color_bar_html += '</div>'

        st.markdown(color_bar_html, unsafe_allow_html=True)

    with legend_col:
        for emotion, (emoticon, color) in EMOTICON_MAP.items():
            if emotion is None:
                continue
            st.write(f"{emoticon} - {emotion.capitalize() if emotion else 'Neutral'}")
            st.markdown(
                f'<div style="background-color:{color}; width: 80%; height: 30px; border-radius: 5px; margin-bottom: 5px;"></div>',
                unsafe_allow_html=True)


def audio_review():
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
    # Mock ze w sesji istnieje jakies video
    st.session_state['CURRENT_VIDEO_UUID'] = "HY_2024_film_01"

    analysis_review()
