import pandas as pd
import re
from transformers import AutoTokenizer

def clean_text(text):
    """ Clean the input text. """
    # Remove unwanted characters (URLs, special symbols)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
    return text

def load_and_clean_data(file_path):
    """ Load and clean the dataset. """
    data = pd.read_csv(file_path)
    data['cleaned_text'] = data['text'].apply(clean_text)
    return data

def get_tokenizer(model_name="roberta-base"):
    """ Get tokenizer for the specified transformer model. """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer
