
import os
from pathlib import Path
import time
from dotenv import load_dotenv
from uuid import UUID

import requests

load_dotenv()

API_URL = os.getenv("API_URL")

def add_video(video_uuid: UUID) -> bool:
    return True
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
