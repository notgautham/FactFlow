# pipeline.py
import os
import pandas as pd
from data_loader import load_dataset
from clean_text import clean_text
from feature_extraction import extract_features

OUTPUT_PATH = os.path.join("ml_model", "dataset", "3", "preprocessed_dataset.csv")

def preprocess_pipeline():
    """
    Load dataset, extract features, clean text, and save processed data.
    """
    df = load_dataset()

    # Extract additional features
    df = extract_features(df)

    # Clean text
    df["cleaned_text"] = df["text"].apply(clean_text)

    # Save processed dataset
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Preprocessed dataset saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    preprocess_pipeline()
