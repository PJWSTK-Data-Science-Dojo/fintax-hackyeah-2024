import os
import logging
import uvicorn
import pathlib
import shutil

from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from uuid import uuid4
from pydantic import BaseModel
from typing import List

from processing import Processing

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)-s %(message)s")

jobs = []
workspace_dir = pathlib.Path(
    "../test_data"
)
workspace_dir.mkdir(parents=True, exist_ok=True)


class VideoAnalysisState(BaseModel):
    video_uuid: str = "0000-4444-0000-4444"

@app.post("/video", tags=["Analysis"])
async def upload_video(video_data: VideoAnalysisState):
    global jobs
    # Create a processing object
    processor = Processing(video_data.video_uuid)
    jobs.append(processor)

    # Start the asynchronous processing and return the ID
    try:
        process_id = await processor.start(video_data.video_uuid, workspace_dir)
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)
    return {"process_id": process_id}

@app.post("/analysis/audio")
async def get_processing_status(video_data: VideoAnalysisState):
    global jobs
    for job in jobs:
        if str(job.id) == video_data.video_uuid:
            return await job.get_processing_stage()
    raise HTTPException(status_code=404, detail="Process not found.")

@app.post("/analysis/video")
async def get_processing_status(video_data: VideoAnalysisState):
    global jobs
    for job in jobs:
        if str(job.id) == video_data.video_uuid:
            return job.get_processing_data()
    raise HTTPException(status_code=404, detail="Process not found.")


# Run the FastAPI application on port 5000
# if __name__ == "__main__":
#   uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, access_log=False)
