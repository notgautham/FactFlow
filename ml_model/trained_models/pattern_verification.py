from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

# Path to your trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_3class_v2")
NUM_CLASSES = 3

# Load model and tokenizer once (not inside function)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Collapse SOFT FAKE into FAKE (you can toggle this if needed)
label_map = {
    0: "FAKE",
    1: "FAKE",  # SOFT FAKE treated as FAKE
    2: "REAL"
}

def analyze_content(text: str) -> dict:
    """
    Takes in news content as input and returns classification output.

    Returns:
        {
            "label": "FAKE" | "REAL",
            "confidence": 0.94,
            "probabilities": {
                "FAKE": 0.94,
                "SOFT_FAKE": 0.03,
                "REAL": 0.03
            }
        }
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = torch.softmax(outputs.logits, dim=1)[0]
    predicted_class = torch.argmax(probs).item()

    return {
        "label": label_map[predicted_class],
        "confidence": round(probs[predicted_class].item(), 4),
        "probabilities": {
            "FAKE": round(probs[0].item(), 4),
            "SOFT_FAKE": round(probs[1].item(), 4),
            "REAL": round(probs[2].item(), 4)
        }
    }
