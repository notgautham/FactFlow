# data_loader.py
import pandas as pd
import os

DATASET_PATH = os.path.join("ml_model", "dataset", "3")  # Ensure this matches your actual dataset location

def load_dataset():
    """
    Loads the Fake and Real news datasets into a single DataFrame with labels.
    """
    fake_path = os.path.join(DATASET_PATH, "Fake.csv")
    real_path = os.path.join(DATASET_PATH, "True.csv")

    # Load datasets
    df_fake = pd.read_csv(fake_path)
    df_real = pd.read_csv(real_path)

    # Add labels (1 = Fake, 0 = Real)
    df_fake["label"] = 1
    df_real["label"] = 0

    # Combine datasets
    df = pd.concat([df_fake, df_real], ignore_index=True)

    return df

if __name__ == "__main__":
    df = load_dataset()
    print("Dataset Loaded. Shape:", df.shape)
    print(df.head())
