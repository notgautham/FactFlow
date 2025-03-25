import sys
import os
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
from datasets import Dataset

# Project structure
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml_model.models.content_model import get_model, train_model
from ml_model.preprocessing.feature_extraction import tokenize_data

# Load dataset
data_path = "ml_model/dataset/3.9/fake_news_3class_15k_final.csv"
df = pd.read_csv(data_path).dropna()

# Tokenizer and model setup
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = get_model("roberta-base", num_labels=3)

# Tokenize and prepare
encodings = tokenize_data(df["text"].tolist(), tokenizer)
labels = torch.tensor(df["label"].values)

train_input_ids, val_input_ids, train_attention_mask, val_attention_mask, train_labels, val_labels = train_test_split(
    encodings['input_ids'], encodings['attention_mask'], labels, test_size=0.1, random_state=42
)

train_dataset = Dataset.from_dict({
    'input_ids': train_input_ids,
    'attention_mask': train_attention_mask,
    'labels': train_labels
})

val_dataset = Dataset.from_dict({
    'input_ids': val_input_ids,
    'attention_mask': val_attention_mask,
    'labels': val_labels
})

# Save model in new structured folder
trainer = train_model(model, train_dataset, val_dataset, tokenizer)
trainer.save_model("ml_model/trained_models/model_3class_v2")
