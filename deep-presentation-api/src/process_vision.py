import logging
import pathlib
import subprocess
import time

from text.ai_textual_report import get_ai_textual_report
from video.frame_processing import get_emotions_report
from audio.get_histogram import get_histogram
from audio.speach_pauses import get_speach_pauses

def split_video_to_frames(video_file_path, tmpdir):
    """
    Split video into frames, one per second.
    """
    input_video = video_file_path
    output_format = "jpg"

    # Construct the ffmpeg command for segmenting the video
    segment_name_template = "frame_%04d"  # Template for output filenames

    ffmpeg_cmd = f'ffmpeg -i {input_video} -vf "fps=1" {tmpdir}/{segment_name_template}.{output_format}'

    # Execute the ffmpeg command
    subprocess.run(
        ffmpeg_cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def process_halves(arr, start=0, end=None, depth=0):
    res = []
    if end is None:
        end = len(arr)

    # Base case: if there's only one element, just print that element
    if end - start <= 1:
        if len(arr[start:end]) > 0:
            res.append(arr[start:end])
        return None

    # Find the middle index
    mid = (start + end) // 2

    # Print the element at the middle index (this is how we "process" it)
    res.append(arr[mid])

    # Recursively process the left and right halves
    l_res = process_halves(arr, start, mid, depth + 1)  # Process the left half
    r_res = process_halves(arr, mid + 1, end, depth + 1)  # Process the right half

    if l_res is not None:
        res.extend(l_res)
    if r_res is not None:
        res.extend(r_res)
    return res


class VisionProcessing:
    def __init__(self):
        self.video_vector_store = None
        self.video_processing_results = {}
        self.video_processing_all_frames_count = 0

    def process_vision(self, video_file_path: pathlib.Path, workdir):
        start_time = time.time()
        tmpdir_vids = pathlib.Path(workdir, "frames")
        tmpdir_vids.mkdir(exist_ok=True)

        logging.info(f"Chunking video to frames")
        split_video_to_frames(video_file_path, tmpdir_vids)
        logging.info(f"Video chunked to frames")

        video_frames = sorted([str(f) for f in pathlib.Path(tmpdir_vids).glob("*.jpg")])
        self.video_processing_all_frames_count = len(video_frames)
        # Process each video chunk
        logging.info(f"Processing video frames")

        # TODO: Process video
        self.video_processing_results['textual_report'] = get_ai_textual_report(video_file_path.stem)

        self.video_processing_results['emotions_report'] = get_emotions_report(video_file_path.stem)

        self.video_processing_results['histogram_data'] = get_histogram(video_file_path.stem)

        self.video_processing_results['pauses_data'] = get_speach_pauses(video_file_path.stem)

        end_time = time.time()
        delta_time = end_time - start_time
        logging.info(f"Processed video frames")
        logging.info(f"Time spent processing video: {delta_time:.2f}")
