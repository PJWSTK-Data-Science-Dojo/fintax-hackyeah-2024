import textstat

def index_flesch(transcription):
    full_text = ""
    for sentence_dict in transcription:
        full_text += sentence_dict['text']
    return textstat.flesch_reading_ease(full_text)

def indexes_fog(transcription):
    full_text = ""
    for sentence_dict in transcription:
        full_text += sentence_dict['text']
    return textstat.gunning_fog(full_text)


