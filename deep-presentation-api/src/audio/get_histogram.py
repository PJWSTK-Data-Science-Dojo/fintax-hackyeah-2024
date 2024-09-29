import os
import pathlib

import numpy as np
from scipy.io import wavfile

VIDEO_STORAGE = pathlib.Path(os.getenv("VIDEO_STORAGE", "test_data"))

def get_histogram(video_uuid):
    path = pathlib.Path(VIDEO_STORAGE, f"{video_uuid}/{video_uuid}.wav")
    sample_rate, signal = wavfile.read(path)

    if len(signal.shape) > 1:
        signal = signal.mean(axis=1)

    signal = signal / np.max(np.abs(signal))

    signal = signal.tolist()

    return {
        "sample_rate": sample_rate,
        "histogram_data": signal
    }
