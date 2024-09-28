
import io
import os
from pathlib import Path
import time
from dotenv import load_dotenv
from uuid import UUID

import requests

load_dotenv()

API_URL = os.getenv("API_URL")

def add_video(video_uuid: UUID) -> bool:
    url = f"{API_URL}/video"
    try:
        response = requests.post(url=url, data={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return True
        
        return False
    except requests.RequestException as rex:
        print(rex)

    return False


def fetch_subtitles(video_uuid: UUID) -> io.BytesIO:

    url = f"{API_URL}/{video_uuid}/subtitles"
    try:
        response = requests.get(url=url)

        if response.status_code == 200:
            return response.content
        
        return io.BytesIO()
    except requests.RequestException as rex:
        print(rex)

    return io.BytesIO()


def fetch_video_analysis(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/video"

    try:
        response = requests.post(url=url, data={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()
        
        return None
    except requests.RequestException as rex:
        print(rex)

    return None


def fetch_audio_analysis(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/audio"

    try:
        response = requests.post(url=url, data={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()
        
        return None
    except requests.RequestException as rex:
        print(rex)

    return None



def fetch_full_analysis(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/full"

    try:
        response = requests.post(url=url, data={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()
        
        return None
    except requests.RequestException as rex:
        print(rex)

    return None