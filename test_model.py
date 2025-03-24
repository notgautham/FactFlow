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
    #print(f"📄 Input: {text}")

if __name__ == "__main__":
    # Example test cases
    sample_texts = [
        """BREAKING: Reports have emerged about cash being found at the residence of Delhi High Court Judge Yashwant Varma. While the official line is that a committee has been formed by the Supreme Court to investigate, the timing and manner of discovery has raised questions among legal observers.

Union Law Minister Arjun Ram Meghwal commented on the matter, stating that “the committee will look into it,” but did not elaborate further. Some insiders have pointed out that this is not the first time such incidents have happened, though no direct accusations have been made.

Sanitation workers reportedly found partially burnt ₹500 notes near the judge’s residence, which they said appeared unexpectedly during routine cleaning. “We found some small pieces,” one worker said. “We don’t really know where they came from.”

Justice Varma has denied any wrongdoing and suggested that the incident may have been intended to harm his reputation. However, the room where the cash was allegedly found was not in the main house, but in a separate building nearby, which has added further speculation online.

The judiciary has yet to make a final determination, but this development has already sparked discussions both in legal circles and on social media. Some legal experts believe the inquiry may reveal more about how such incidents are handled within the system.

"""
    ]

    for text in sample_texts:
        predict(text)
