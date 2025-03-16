# feature_extraction.py
import re
import pandas as pd

def count_uppercase_words(text):
    """
    Count the number of uppercase words in the given text.
    """
    words = text.split()
    uppercase_words = [word for word in words if word.isupper()]
    return len(uppercase_words), len(uppercase_words) / max(len(words), 1)  # Avoid division by zero

def extract_features(df):
    """
    Extract additional features such as uppercase word ratio.
    """
    df["uppercase_count"], df["uppercase_ratio"] = zip(*df["text"].apply(count_uppercase_words))
    return df

if __name__ == "__main__":
    # Example test
    sample_text = "BREAKING NEWS: This is a FAKE story with some REAL elements."
    print(count_uppercase_words(sample_text))  # Expected output: (3, ratio)
