# content_model.py
# Defines the content-based fake news detection model using a transformer architecture.

from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "roberta-large"  # or "microsoft/deberta-v3-base" for a DeBERTa variant

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

def predict(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    prediction = outputs.logits.argmax().item()
    return prediction

if __name__ == "__main__":
    sample_text = "The quick brown fox jumps over the lazy dog!"
    print("Prediction (0: Real, 1: Fake):", predict(sample_text))
