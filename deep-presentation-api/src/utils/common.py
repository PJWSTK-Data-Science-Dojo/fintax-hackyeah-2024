import functools
import json
import pathlib
import os

VIDEO_STORAGE = pathlib.Path(os.getenv("VIDEO_STORAGE", "test_data"))

def get_ts_from_path(video_frame_file_path):
    return int(str(pathlib.Path(video_frame_file_path).stem).split("_")[1])


@functools.cache
def get_transcription(video_uuid) -> str:
    path = pathlib.Path(VIDEO_STORAGE, f"{video_uuid}/transcription.json")
    with open(path, "r") as json_file:
        data = json.load(json_file)

    return " ".join(item["text"] for item in data)
