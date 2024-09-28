import io
from pathlib import Path
from uuid import UUID, uuid4
import os
from dotenv import load_dotenv
from utils import api
load_dotenv()

VIDEO_STORAGE = Path(os.getenv("VIDEO_STORAGE"))
if not VIDEO_STORAGE.exists():
    VIDEO_STORAGE.mkdir()


def create_video(video_buffer: io.BytesIO) -> UUID:
    video_uuid = uuid4()
    video_uuid = uuid4()
    uuid_catalog_path = VIDEO_STORAGE / str(video_uuid)
    uuid_catalog_path.mkdir(parents=True, exist_ok=True)

    uuid_video_path = uuid_catalog_path / f"{video_uuid}.mp4"

    with uuid_video_path.open(mode="wb") as f:
        f.write(video_buffer.getbuffer())

    success = api.add_video(video_uuid=video_uuid)
    if not success:
        return None

    return video_uuid
