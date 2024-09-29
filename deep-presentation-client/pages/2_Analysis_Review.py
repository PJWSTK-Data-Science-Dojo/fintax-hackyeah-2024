import os
import time
from pathlib import Path

import numpy as np
import plotly.express as px
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


def render_textual_analysis(textual_report):
    container = st.container()
    with container:
        st.markdown("### 📊 Raport analizy tekstowej")

        # Sekcja z poradami AI
        with st.expander("💡 Porady AI", expanded=True):
            ai_advice = textual_report.get('ai_advice', 'Brak porad AI.')
            st.markdown(
                f"""
                <div style="padding: 10px; border-left: 4px solid #3498db;">
                    <p style="font-size: 15px; line-height: 1.5;">{ai_advice}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Sekcja ze znalezionymi błędami
        with st.expander("⚠️ Znalezione błędy", expanded=True):
            st.markdown("**W raporcie znaleziono następujące problemy:**")
            st.checkbox("Użyto zbyt wielu liczb", value=textual_report.get('too_many_numbers_usesd', False),
                        disabled=True)
            st.checkbox("Wykryto zmianę tematu", value=textual_report.get('chage_of_topic', False), disabled=True)
            st.checkbox("Wykryto powtórzenia", value=textual_report.get('repetitions', False), disabled=True)
            st.checkbox("Użyto strony biernej", value=textual_report.get('passive_voice', False), disabled=True)

        with st.expander("❓ Dalsze pytania do rozważenia"):
            further_questions = textual_report.get('further_questions', 'Brak pytań.')
            questions_list = [q.strip() for q in further_questions.split('\n') if q.strip()]
            if questions_list:
                html_content = """
                <div style="padding: 10px; border-left: 4px solid #f39c12;">
                    <ul style="font-size: 15px; line-height: 1.5; margin: 0; padding-left: 20px;">
                """
                for question in questions_list:
                    html_content += f"<li style='margin-bottom: 8px;'>{question}</li>"
                html_content += """
                    </ul>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.markdown(
                    """
                    <div style="padding: 10px; border-left: 4px solid #f39c12;">
                        <p style="font-size: 15px; line-height: 1.5;">Brak pytań.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Sekcja z grupą docelową
        with st.expander("🎯 Grupa docelowa"):
            target_audience = textual_report.get('target_audienc', 'Nie określono')
            st.markdown(
                f"""
                <div style="padding: 10px; border-left: 4px solid #2ecc71;">
                    <p style="font-size: 15px; font-weight: bold;">Grupa docelowa:</p>
                    <p style="font-size: 14px;">{target_audience}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


def video_review(video_analysis):
    video_col = st.columns(1)[0]
    render_emotions_and_legend(video_col, video_analysis['video']['emotions_report']['frames'])


def render_audio_histogram(histogram_data):
    histogram = histogram_data['histogram_data']
    sample_rate = histogram_data['sample_rate']

    time_axis = np.linspace(0, len(histogram) / sample_rate, num=len(histogram))

    histogram_df = {
        "Time (s)": time_axis,
        "Amplitude": histogram
    }

    fig = px.line(
        histogram_df,
        x="Time (s)",
        y="Amplitude",
        title='Audio Histogram',
        template='plotly_dark',
        line_shape='spline'
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)


def render_pauses_data(pauses, video_duration):
    color_list = []
    current_time = 0.0
    for pause in pauses:
        if pause['start_break'] > current_time:
            segment_duration = pause['start_break'] - current_time
            color_list.append(('#3498db', segment_duration))  # Speech color
        segment_duration = pause['end_break'] - pause['start_break']
        color_list.append(('#2c3e50', segment_duration))  # Pause color
        current_time = pause['end_break']

    if current_time < video_duration:
        color_list.append(('#3498db', video_duration - current_time))

    legend_html = """
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; margin-right: 15px;">
                <div style="width: 20px; height: 20px; background-color: #3498db; margin-right: 5px;"></div>
                <span>Mowa</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 20px; height: 20px; background-color: #2c3e50; margin-right: 5px;"></div>
                <span>Pauza</span>
            </div>
        </div>
        """

    # Display legend
    st.markdown(legend_html, unsafe_allow_html=True)

    # Render the color bar
    color_bar_html = '<div style="display: flex; justify-content: center; align-items: center; width: 100%;">'
    for color, duration in color_list:
        width_percentage = (duration / video_duration) * 100
        color_bar_html += f'<div style="flex: {width_percentage}; height: 30px; background-color: {color};"></div>'
    color_bar_html += '</div>'

    st.markdown(color_bar_html, unsafe_allow_html=True)

    average_pause_length = np.mean([pause['break_length'] for pause in pauses])
    max_pause_length = max([pause['break_length'] for pause in pauses])
    col1, col2, col3 = st.columns(3)
    col1.metric("Ilość pauz", f"{len(pauses)}")
    col2.metric("Średnia długość pauzy", f"{average_pause_length:.2f} s")
    col3.metric("Najdłuższa pauza", f"{max_pause_length:.2f} s")


def audio_review(video_analysis):
    pauses = video_analysis['video']['pauses_data']
    histogram_data = video_analysis['video']['histogram_data']['histogram_data']
    video_length = len(video_analysis['video']['emotions_report']['frames'])
    render_pauses_data(pauses, video_length)
    render_audio_histogram(histogram_data)


def full_review(video_analysis):
    render_textual_analysis(video_analysis['video']['textual_report'])


def analysis_review():
    st.set_page_config(layout="wide")

    st.title("Analiza filmu")

    if "video_uuid" not in st.session_state or not st.session_state.video_uuid:
        st.switch_page("pages/1_Upload.py")

    with st.spinner("Analiza w toku..."):
        while True:
            stage_response = api.fetch_analysis_stage(str(st.session_state.video_uuid))
            stages = stage_response.get("stages", [])
            if any(stage.get("stage") == "done_visual" for stage in stages):
                break
            time.sleep(1)

    data_analysis = api.fetch_video_analysis_data(st.session_state.video_uuid)

    subtitles_path = Path(f"{VIDEO_STORAGE}/{st.session_state.video_uuid}/{st.session_state.video_uuid}.srt")
    with st.spinner("Pobieranie napisów..."):
        while not subtitles_path.exists():
            time.sleep(2)


    st.video(st.session_state.uploaded_video, subtitles={
        "Polish": subtitles_path
    })

    video_tab, audio_tab, text_tab = st.tabs(["Video", "Mowa", "Pełna analiza"])

    with video_tab:
        video_review(data_analysis)

    with audio_tab:
        audio_review(data_analysis)

    with text_tab:
        full_review(data_analysis)


if __name__ == "__main__":
    analysis_review()
