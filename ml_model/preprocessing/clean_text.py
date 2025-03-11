import re
import spacy

nlp = spacy.load("en_core_web_sm")

def remove_html_tags(text: str) -> str:
    """Remove HTML tags using regex."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def clean_text(text: str) -> str:
    """
    Clean and preprocess the input text.
    - Remove HTML tags
    - Lowercase text
    - Tokenize and lemmatize using spaCy
    - Remove stop words
    """
    text = remove_html_tags(text)
    text = text.lower()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

if __name__ == "__main__":
    sample = "<p>Breaking news: The <strong>quick</strong> brown fox jumps over the lazy dog!</p>"
    print("Cleaned Text:", clean_text(sample))
