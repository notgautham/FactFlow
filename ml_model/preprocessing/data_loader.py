from datasets import Dataset
from preprocessing.clean_text import load_and_clean_data, get_tokenizer
from preprocessing.feature_extraction import tokenize_data
from sklearn.model_selection import train_test_split
import pandas as pd
import torch

def load_data(fake_file, true_file):
    fake_data = load_and_clean_data(fake_file)
    true_data = load_and_clean_data(true_file)
    
    # Assign labels: 0 for fake, 1 for true
    fake_data['label'] = 0
    true_data['label'] = 1
    
    # Combine both datasets
    data = pd.concat([fake_data[['cleaned_text', 'label']], true_data[['cleaned_text', 'label']]], ignore_index=True)
    
    return data

def prepare_dataset(data, tokenizer):
    """ Prepare the dataset by tokenizing the text and splitting into train/test. """
    encodings = tokenize_data(data['cleaned_text'], tokenizer)
    labels = torch.tensor(data['label'].values)
    
    # Ensure encodings and labels have the same number of entries
    print(f"Length of encodings: {len(encodings['input_ids'])}")
    print(f"Length of labels: {len(labels)}")
    
    # Ensure encodings and labels have the same number of entries
    assert len(encodings['input_ids']) == len(labels), f"Mismatch: {len(encodings['input_ids'])} vs {len(labels)}"
    
    # Split data into train and validation using individual arrays (input_ids, attention_mask, and labels)
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']

    # Now we can split correctly
    train_input_ids, val_input_ids, train_attention_mask, val_attention_mask, train_labels, val_labels = train_test_split(
        input_ids, attention_mask, labels, test_size=0.1, random_state=42
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
    
    return train_dataset, val_dataset
