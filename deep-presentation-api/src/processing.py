import logging
import threading
import pathlib

from process_vision import VisionProcessing
from process_audio import AudioProcessing

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

import asyncio
from uuid import uuid4


class Processing:
    def __init__(self, uuid_id):
        self.id = uuid_id
        self.stages = [
            {
                "stage": "started_initialized",
                "time": datetime.now().strftime("%H:%M:%S"),
            }
        ]
        self.vision_processing = VisionProcessing()
        self.audio_processing = AudioProcessing()

    async def get_processing_stage(self):
        return {
            "video_frames_processed": len(
                self.vision_processing.video_processing_results
            ),
            "video_frames_all": self.vision_processing.video_processing_all_frames_count,
            "stages": self.stages,
        }

    async def get_processing_data(self):
        return {
            "video": self.vision_processing.video_processing_results,
            # "audio": self.audio_processing.audio_processing_results,
        }

    async def start(self, video_file_name, workspace_dir):

        # Generate a unique filename
        filename = self.id + ".mp4"
        self.process_workdir = pathlib.Path(workspace_dir, self.id)
        self.video_path = pathlib.Path(self.process_workdir, filename)
        
        self.stages = [
            {"stage": "done_initialized", "time": datetime.now().strftime("%H:%M:%S")}
        ]
        logging.info(f"Process started. ID: {self.id}")
        # await self.process_audio_visual()
        threading.Thread(target=self.process_audio_visual).start()
        return self.id

    def process_audio_visual(self):
        # Processing audio
        self.stages.append(
            {"stage": "started_audio", "time": datetime.now().strftime("%H:%M:%S")}
        )
        logging.info(f"{self.stages[-1]['stage']} - {self.id}")
        self.audio_processing.process_audio(self.video_path)
        self.stages.append(
            {"stage": "done_audio", "time": datetime.now().strftime("%H:%M:%S")}
        )
        logging.info(f"{self.stages[-1]['stage']} - {self.id}")
        # Processing video
        self.stages.append(
            {"stage": "started_visual", "time": datetime.now().strftime("%H:%M:%S")}
        )
        logging.info(f"{self.stages[-1]['stage']} - {self.id}")
        self.vision_processing.process_vision(self.video_path, self.process_workdir)
        self.stages.append(
            {"stage": "done_visual", "time": datetime.now().strftime("%H:%M:%S")}
        )
        logging.info(f"{self.stages[-1]['stage']} - {self.id}")
        # logging.info(self.get_processing_data())
        # Processing data with llms 
