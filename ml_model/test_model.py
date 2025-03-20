import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F

# Load the trained model and tokenizer
MODEL_PATH = "C:/Gautham/Sem6/Project Course/FactFlow/ml_model/model"  # Adjust based on where your model is saved
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()  # Set model to evaluation mode

def predict_news(text):
    """Tokenize input text and get prediction from the model."""
    inputs = tokenizer(text, truncation=True, padding=True, max_length=512, return_tensors="pt")  # Convert text to tensors
    
    with torch.no_grad():  # No need to compute gradients for inference
        outputs = model(**inputs)
    
    logits = outputs.logits  # Get raw model outputs
    probabilities = F.softmax(logits, dim=-1)  # Convert to probabilities
    
    fake_prob = probabilities[0][0].item()
    real_prob = probabilities[0][1].item()
    
    return {"fake_probability": fake_prob, "real_probability": real_prob}

# Example: Test with a sample news article
if __name__ == "__main__":
    test_text = """This is a test"""
    
    result = predict_news(test_text)
    print(f"Predicted Probabilities: {result}")



