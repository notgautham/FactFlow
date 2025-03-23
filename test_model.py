# test_model.py
# This script loads the trained RoBERTa model and performs predictions on custom input text.

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the trained model and tokenizer
MODEL_PATH = "./model"
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

def predict(text):
    """Predict whether the input text is FAKE or REAL news."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    confidence = torch.softmax(logits, dim=1)[0][predicted_class].item()
    
    label = "REAL" if predicted_class == 1 else "FAKE"
    print(f"\n🧠 Prediction: {label}")
    print(f"🔎 Confidence: {confidence:.2f}")
    print(f"📄 Input: {text}")

if __name__ == "__main__":
    # Example test cases
    sample_texts = [
        "BREAKING: Scientists reveal shocking side effects of the new vaccine!",
        "India's GDP growth projected at 7.2% by IMF this quarter!!!!!!!!!!!!!!.",
        "You won't believe what this celebrity said about the president!!!",
        "According to the World Health Organization, COVID-19 vaccines are safe and effective"
    ]

    for text in sample_texts:
        predict(text)
