import pathlib
import os
import json

VIDEO_STORAGE = pathlib.Path(os.getenv("VIDEO_STORAGE", "test_data"))

def get_speach_pauses(video_uuid):
    path = pathlib.Path(VIDEO_STORAGE, f"{video_uuid}/transcription.json")
    with open(path, "r") as json_file:
        data = json.load(json_file)

    pauses = []

    for sentence_chunk in data:
        timestamp_last_word_end = -1

        for word_data in sentence_chunk['words']:
            timestamp_word_start = -1

            if 'start' in word_data:
                timestamp_word_start = word_data['start']

            if timestamp_last_word_end != -1 and timestamp_word_start != -1:
                break_length = timestamp_word_start - timestamp_last_word_end

                if break_length > 2:
                    pauses.append({
                        "start_break": timestamp_last_word_end,
                        "end_break": timestamp_word_start,
                        "break_length": break_length,
                    })

            if 'end' in word_data:
                timestamp_last_word_end = word_data['end']

    return pauses
