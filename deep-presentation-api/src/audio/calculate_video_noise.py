import numpy as np
import pathlib
import os

from scipy.io import wavfile


VIDEO_STORAGE = pathlib.Path(os.getenv("VIDEO_STORAGE", "test_data"))


def _calculate_snr(signal):
    rms_signal = np.sqrt(np.mean(signal ** 2))
    rms_noise = np.sqrt(np.mean((signal - np.mean(signal)) ** 2))

    if rms_noise == 0:
        return float('inf')

    snr = 20 * np.log10(rms_signal / rms_noise)
    return snr


def get_nsr(video_uuid):
    path = pathlib.Path(VIDEO_STORAGE, f"{video_uuid}/{video_uuid}.wav")
    _sample_rate, signal = wavfile.read(path)

    if signal.ndim == 2:
        signal = signal.mean(axis=1)

    return _calculate_snr(signal)
