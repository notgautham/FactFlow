import pandas as pd
import re
from transformers import AutoTokenizer

def clean_text(text):
    """Clean the input text while keeping important fake news indicators."""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # Preserve punctuation (.,!?), remove other symbols
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def load_and_clean_data(file_path):
    """Load and clean the dataset."""
    data = pd.read_csv(file_path)

    # Drop rows with missing 'text' column to avoid runtime errors
    if 'text' not in data.columns:
        raise ValueError(f"'text' column not found in file: {file_path}")

    data = data.dropna(subset=['text'])
    data['cleaned_text'] = data['text'].apply(clean_text)

    return data

def get_tokenizer(model_name="roberta-base"):
    """Get tokenizer for the specified transformer model."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer
