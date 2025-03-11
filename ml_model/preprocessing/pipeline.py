# pipeline.py
import os
import pandas as pd
from clean_text import clean_text
from data_loader import load_dataset

def preprocess_pipeline(dataset_dir: str, output_csv: str):
    """
    Loads all CSV files from a directory, preprocesses the content, and writes to a new CSV.
    """
    all_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith('.csv')]
    dfs = []
    for file in all_files:
        df = pd.read_csv(file)
        # Assuming a 'content' column exists
        df['cleaned_content'] = df['content'].apply(clean_text)
        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_csv(output_csv, index=False)
    print(f"Preprocessed dataset saved to {output_csv}")

if __name__ == "__main__":
    # Example usage: Merge and preprocess all datasets in ml_model/dataset/2/
    dataset_directory = os.path.join("ml_model", "dataset", "2")
    output_file = os.path.join(dataset_directory, "preprocessed_dataset.csv")
    preprocess_pipeline(dataset_directory, output_file)
