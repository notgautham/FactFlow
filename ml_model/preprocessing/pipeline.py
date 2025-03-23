# pipeline.py — Optional CLI wrapper for debugging the data pipeline
import os
from preprocessing.data_loader import load_data
from preprocessing.clean_text import get_tokenizer

if __name__ == "__main__":
    fake_file = "./ml_model/dataset/3.2/Fake_enhanced_v2.csv"
    true_file = "./ml_model/dataset/3/True.csv"

    tokenizer = get_tokenizer("roberta-base")

    data = load_data(fake_file, true_file)

    print("✅ Dataset Loaded Successfully")
    print("Sample Data:\n", data.sample(3))
    print("\nLabel Distribution:\n", data['label'].value_counts())
