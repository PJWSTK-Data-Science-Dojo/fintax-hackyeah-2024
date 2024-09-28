import pathlib
from deepface import DeepFace
from collections import Counter
import os
from typing import List

VIDEO_STORAGE =  pathlib.Path(os.getenv("VIDEO_STORAGE"))

def get_emotions_report(video_uuid, start_from_farme_in_seconds: int=0):
    dir = f"{VIDEO_STORAGE}/{video_uuid}/frames" # change 'test_data' later

    report_data = {}
    report_data['frames'] = []
    emotions_list: List[str] = []

    for i, filename in enumerate(sorted(os.listdir(dir)), 1):
        if i < start_from_farme_in_seconds:
            continue

        file_path = os.path.join(dir, filename)
        result = None
        try:
            result = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=True)
            result = result[0]['dominant_emotion']
            emotions_list.append(result)
        except ValueError as value_error:
            print(f"No face detected in the frame: {value_error} ({video_uuid})")
        except Exception as e:
            print(f"Error processing frame: {e} ({video_uuid})")
        finally:
            report_data['frames'].append({
                "start": i-1,
                "end": i,
                "emotion": result
            })

    dominant_emotion: str = Counter(emotions_list).most_common(1)[0][0]
    report_data['dominant_emotion'] = dominant_emotion

    return report_data
