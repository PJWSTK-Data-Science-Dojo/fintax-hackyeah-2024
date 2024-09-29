import numpy as np
from scipy.io import wavfile
import pathlib
import os

VIDEO_STORAGE = pathlib.Path(os.getenv("VIDEO_STORAGE", "test_data"))

def get_histogram(video_uuid):
    path = pathlib.Path(VIDEO_STORAGE, f"{video_uuid}/{video_uuid}.wav")
    sample_rate, data = wavfile.read(path)

    # Check if the audio is stereo or mono
    if len(data.shape) > 1:
        # Stereo audio, select one channel or average both
        data = data.mean(axis=1)  # Averaging both channels

    #  Normalize the data
    data = data / np.max(np.abs(data))

    return {
        "sample_rate": sample_rate,
        "histogram_data": data
    }
