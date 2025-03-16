# clean_text.py
import re
import spacy

nlp = spacy.load("en_core_web_sm")  # Use SpaCy for tokenization & lemmatization

def clean_text(text):
    """
    Cleans text: removes special characters, tokenizes, and lemmatizes.
    Does NOT lowercase everything to preserve uppercase word analysis.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    doc = nlp(text)
    
    # Lemmatize words
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    
    return " ".join(tokens)

if __name__ == "__main__":
    sample_text = "BREAKING NEWS: This is a FAKE story with some REAL elements."
    print("Cleaned Text:", clean_text(sample_text))
