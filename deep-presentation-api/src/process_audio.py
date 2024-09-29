import os
import pathlib
import requests
import librosa
import numpy as np
import subprocess
import logging
import time
import json
from audio.find_similiar_sentences_transcription import find_similiar_sentences
from audio.indexes import indexes_scoring
from audio.srt_gen import gen_srt_file

from dotenv import load_dotenv
load_dotenv()

def whisperx_inference(audio_file_path):
    url = os.environ.get("WHISPERX_API") + "/transcribe/"
    print(url)
    # Open the audio file in binary mode and send it via a POST request
    with open(audio_file_path, "rb") as audio_file:
        # Prepare the files parameter for the POST request
        files = {
            "file": (audio_file_path, audio_file, "audio/wav")
        }

        # Send the request to the FastAPI server
        response = requests.post(url, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print the transcription result from the API response
            return json.loads(response.json())
        else:
            print("Error:", response.status_code, response.text)

def analyze_audio(file_path):
    """Analyzes an audio file for loudness and returns a list of chunks with loudness values.

    Args:
        file_path (str): The path to the audio file.

    Returns:
        list: A list of tuples, where each tuple contains the start time, end time, and loudness value for a chunk.
    """

    # Load the audio file
    y, sr = librosa.load(file_path)

    # Calculate the root mean square (RMS) energy of the audio signal
    rms = librosa.feature.rms(y=y)[0]

    # Normalize the RMS values to a range of 0 to 1
    normalized_rms = rms / np.max(rms)

    # Define chunk size in seconds
    chunk_size = 0.5

    # Calculate the number of frames per chunk (based on RMS resolution)
    hop_length = 512  # Default hop_length used by librosa.feature.rms
    frames_per_chunk = int((chunk_size * sr) / hop_length)

    # Divide the audio into chunks and calculate loudness for each chunk
    chunks = []
    for i in range(0, len(normalized_rms), frames_per_chunk):
        end_frame = min(i + frames_per_chunk, len(normalized_rms))
        start_time = float(
            librosa.frames_to_time(i, sr=sr, hop_length=hop_length)
        )  # Convert to native Python float
        end_time = float(
            librosa.frames_to_time(end_frame, sr=sr, hop_length=hop_length)
        )  # Convert to native Python float
        loudness = float(
            np.mean(normalized_rms[i:end_frame])
        )  # Convert to native Python float

        chunks.append([start_time, end_time, loudness])

    return chunks


class AudioProcessing:
    def __init__(self):
        self.audio_vector_store = None
        self.audio_processing_results = {}


    def process_audio(self, video_path: pathlib.Path):
        """
        Run pipeline to get data from audio.
        """
        start_time = time.time()
        wav_audio_path = video_path.with_suffix(".wav")
        logging.info("Splitting audio from video")
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-y",
                wav_audio_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logging.info("Splitted audio from video")

        # Transcribe audio file to text
        logging.info("Running transcription")
        # with open(video_path.with_name("transcription").with_suffix(".json")) as f:
        #     transcription = json.loads(f.read())
        transcription = whisperx_inference(str(wav_audio_path))
        print(transcription)
        gen_srt_file(transcription, video_path.with_suffix(".srt"))
        self.audio_processing_results['srt_ready'] = True

        transcription = whisperx_inference(wav_audio_path)

        if transcription is None:
            raise RuntimeError("Transcription failed")
        logging.info("Transcription done")

        # Generate Loud / Silent labels
        # logging.info("Generate Loud / Silent labels")
        # loudness_data = analyze_audio(wav_audio_path)
        # logging.info("Generated Loud / Silent labels")

        self.audio_processing_results["similar_sentences_after_each_other"] = find_similiar_sentences(transcription)
        self.audio_processing_results["indexes"] = indexes_scoring(transcription)

        end_time = time.time()
        delta_time = end_time - start_time
        logging.info(f"Time spent processing audio: {delta_time:.2f}")
