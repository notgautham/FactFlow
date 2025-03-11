# clean_text.py
# This module provides functions for cleaning and preprocessing article text.

import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Clean the input text by lowercasing, removing unwanted characters, and lemmatizing.
    """
    doc = nlp(text)
    cleaned = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return cleaned

if __name__ == "__main__":
    sample = "Breaking news: The quick brown fox jumps over the lazy dog!"
    print("Cleaned Text:", clean_text(sample))
