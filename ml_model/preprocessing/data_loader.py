# data_loader.py
# This module loads and merges datasets from the specified CSV files.

import pandas as pd
import os

def load_dataset(path: str) -> pd.DataFrame:
    """
    Load a CSV dataset from the given path.
    """
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        raise FileNotFoundError(f"{path} not found.")

if __name__ == "__main__":
    # Example usage:
    dataset_path = os.path.join(os.getcwd(), "ml_model", "dataset", "2", "expanded_dataset.csv")
    try:
        df = load_dataset(dataset_path)
        print("Dataset loaded successfully with shape:", df.shape)
    except Exception as e:
        print(e)
