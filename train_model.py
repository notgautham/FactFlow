import sys
import os

# Add the 'ml_model' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_model'))

from preprocessing.data_loader import load_data, prepare_dataset
from models.content_model import get_model, train_model
from transformers import AutoTokenizer

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = get_model("roberta-base", num_labels=2)

# Updated file paths to use the enhanced dataset
fake_file = "./ml_model/dataset/3.2/Fake_enhanced_v2.csv"
true_file = "./ml_model/dataset/3/True.csv"

# Load and preprocess the data
data = load_data(fake_file, true_file)
# Sample a smaller dataset
data = data.sample(n=1000, random_state=42)  # Try 1000–3000 samples max


# Prepare dataset using full data
train_dataset, val_dataset = prepare_dataset(data, tokenizer)

# Train the model
trainer = train_model(model, train_dataset, val_dataset, tokenizer)

# Save the model
trainer.save_model("./model")
