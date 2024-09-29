import textstat

def indexes_scoring(transcription):
    full_text = ""
    for sentence_dict in transcription:
        full_text += sentence_dict['text']

    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(full_text),
        "gunning_fog_index": textstat.gunning_fog(full_text)
    }


