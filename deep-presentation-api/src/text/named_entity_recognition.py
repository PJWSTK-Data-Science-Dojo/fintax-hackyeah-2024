import spacy
from typing import Dict, List

from utils.common import get_transcription


def _get_ner():
    return spacy.load("pl_core_news_sm")


def compute_ner(video_uuid) -> Dict[str, List[str]]:
    input: str = get_transcription(video_uuid)
    ner_model = _get_ner()

    works_of_art, people, phrases = [], [], []

    for ent in ner_model(input).ents:
        if ent.label_ == "WORK_OF_ART":
            works_of_art.append(ent.text)
        elif ent.label_ == "PERSON":
            people.append(ent.text)
        elif ent.label_ == "PRODUCT":
            phrases.append(ent.text)
        elif ent.label_ == "LOC":
            phrases.append(ent.text)
        elif ent.label_ == "GPE":
            phrases.append(ent.text)
        elif ent.label_ == "ORG":
            phrases.append(ent.text)

    return {
        "works_of_art": works_of_art,
        "people": people,
        "phrases": phrases,
    }
