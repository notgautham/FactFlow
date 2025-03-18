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

# Load and preprocess the data
fake_file = "C:/Gautham/Sem6/Project Course/FactFlow/ml_model/dataset/3/Fake.csv"
true_file = "C:/Gautham/Sem6/Project Course/FactFlow/ml_model/dataset/3/True.csv"
data = load_data(fake_file, true_file)
train_dataset, val_dataset = prepare_dataset(data, tokenizer)

# Train the model
trainer = train_model(model, train_dataset, val_dataset, tokenizer)  # Pass tokenizer here

# Save the model
trainer.save_model("./model")
