import io
import os
from uuid import UUID

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def add_video(video_uuid: UUID) -> bool:
    url = f"{API_URL}/video"

    data = {
        "video_uuid": str(video_uuid)
    }

    try:
        response = requests.post(url=url, json=data)

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


def fetch_analysis_stage(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/stage"

    try:
        response = requests.post(url=url, json={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()

        return None
    except requests.RequestException as rex:
        print(rex)

    return None


def fetch_analysis_data(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/data"

    try:
        response = requests.post(url=url, json={
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
        response = requests.post(url=url, json={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()

        return None
    except requests.RequestException as rex:
        print(rex)

    return None

def fetch_video_analysis_data(video_uuid: UUID) -> dict | None:
    url = f"{API_URL}/analysis/data"

    try:
        response = requests.post(url=url, json={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()

        return None
    except requests.RequestException as rex:
        print(rex)

    return None

def fetch_analysis_stage(video_uuid):
    url = f"{API_URL}/analysis/stage"

    try:
        response = requests.post(url=url, json={
            "video_uuid": video_uuid
        })

        if response.status_code == 200:
            return response.json()

        return None
    except requests.RequestException as rex:
        print(rex)

    return None
