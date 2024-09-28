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
    "project/data"
)
workspace_dir.mkdir(parents=True, exist_ok=True)


@app.post("/analysis", tags=["Analysis"])
async def upload_video(video_file: UploadFile = File(...)):
    global jobs

    # Create a processing object
    processor = Processing()
    jobs.append(processor)

    # Start the asynchronous processing and return the ID
    try:
        process_id = await processor.start(video_file, workspace_dir)
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)
    return {"process_id": process_id}


@app.get("/analysis/stage/{process_id}")
async def get_processing_status(process_id: str):
    global jobs
    for job in jobs:
        if str(job.id) == process_id:
            return await job.get_processing_stage()
    raise HTTPException(status_code=404, detail="Process not found.")

@app.get("/analysis/data/{process_id}")
async def get_processing_status(process_id: str):
    global jobs
    for job in jobs:
        if str(job.id) == process_id:
            return job.get_processing_data()
    raise HTTPException(status_code=404, detail="Process not found.")


# Run the FastAPI application on port 5000
if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, access_log=False)
