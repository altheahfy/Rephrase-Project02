
import spacy
from rephrase_mapper import map_to_rephrase_slots

nlp = spacy.load("en_core_web_sm")

def analyze_slotphrase(slotphrase):
    doc = nlp(slotphrase)
    return map_to_rephrase_slots(doc)
