def get_ts_from_path(video_frame_file_path):
    return int(str(pathlib.Path(video_frame_file_path).stem).split("_")[1])