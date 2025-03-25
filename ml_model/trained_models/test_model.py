from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Point to the trained model
MODEL_PATH = "ml_model/trained_models/model_3class_v2"
NUM_CLASSES = 3

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Collapse 3-class into binary for interpretation
label_map = {
    0: "FAKE",
    1: "FAKE",  # SOFT FAKE treated as FAKE
    2: "REAL"
} if NUM_CLASSES == 3 else {
    0: "FAKE",
    1: "REAL"
}

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)[0]

    predicted_class = torch.argmax(probs).item()
    confidence = probs[predicted_class].item()
    label = label_map[predicted_class]

    print(f"\n🧠 Prediction: {label}")
    print(f"🔎 Confidence: {confidence:.2f}")
    print(f"📊 Class Probabilities → FAKE: {probs[0]:.2f} | SOFT FAKE: {probs[1]:.2f} | REAL: {probs[2]:.2f}")


if __name__ == "__main__":
    test_cases = [
        """SHOCKING NEWS: New global report reveals secret meetings between government officials and foreign investors!!!""",
        """Observers have raised concerns about the sudden decision to revise fuel subsidies just days before the parliamentary session.""",
        """The Ministry of Health and Family Welfare announced the successful rollout of 50 million COVID-19 vaccine doses.""",
        """Some sources have suggested that the recent budget speech was crafted to mislead the public about inflation.""",
        """EXCLUSIVE: You won’t believe what was discovered in the recent intelligence debrief!!!""",
        """hello this is a text ecample nd I am using a very horrible grammar nd i not know how to type porpely!!!"""
    ]

    for text in test_cases:
        predict(text)
