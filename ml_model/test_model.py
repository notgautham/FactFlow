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
    test_text = """Photo Credit: AFP

President Donald Trump and Russian President Vladimir Putin agreed during their call on Tuesday (March 18, 2025) to seek a limited ceasefire against energy and infrastructure targets in the Russia-Ukraine war, according to the White House.

The Kremlin said the two leaders had a “detailed and frank exchange of views”. Mr. Putin outlined a number of conditions for a possible ceasefire, including “the need to halt both forced mobilisation in Ukraine and the rearmament of the Ukrainian armed forces”.

Listen | What’s in the 30-day ceasefire proposal for Russia, Ukraine and Europe? | In Focus podcast

Mr. Trump proposed a 30-day halt on strikes on energy targets and “Putin responded positively and immediately gave the Russian military a corresponding command”, the statement added.

Russia and Ukraine will also swap 175 prisoners each on Wednesday, the Kremlin said.

The White House described it as the first step in a “movement to peace” it hopes will eventually include a maritime ceasefire in the Black Sea and a full and lasting end to the fighting.

The White House said negotiations would “begin immediately” on those steps. It was not immediately clear whether Ukraine is on board with the phased ceasefire plan.

Mr. Putin also called on Mr. Trump to end foreign military and intelligence assistance to Ukraine as the U.S. looks to bring an end to Russia’s invasion of Ukraine, according to the Kremlin.

 Volodymyr Zelenskyy | Twisting in the whirlwind

Earlier, Mr. Trump, before the call, said he expected to discuss with Mr. Putin land and power plants that have been seized during the grinding three-year war.

Zelenskyy says Ukraine would support a U.S. proposal
President Volodymyr Zelenskyy said Ukraine would support a U.S. proposal to stop strikes on Russian energy infrastructure, and that he hoped to speak to U.S. President Donald Trump about his phone call on Tuesday with Russian President Vladimir Putin.

“...The two sides, Ukraine and Russia, are able to not strike energy infrastructure. Our side will support this,” Mr. Zelenskyy told reporters during an online briefing.

He added that Ukraine would support any proposals that lead to a “stable and just peace.”

“I think it will be right that we will have a conversation with President Trump and we will know in detail what the Russians offered the Americans or what the Americans offered the Russians,” says Mr. Zelenskyy"""
    
    result = predict_news(test_text)
    print(f"Predicted Probabilities: {result}")



