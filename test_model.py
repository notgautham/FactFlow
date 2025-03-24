from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Toggle between models
MODEL_PATH = "./model_3class"   # Change to "./model" to test binary classifier
NUM_CLASSES = 3                 # Set to 2 for binary model

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Label mapping for 3-class
label_map = {
    0: "FAKE",
    1: "SOFT FAKE",
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
    probs = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(probs, dim=1).item()
    confidence = probs[0][predicted_class].item()
    
    label = label_map[predicted_class]
    print(f"\n🧠 Prediction: {label}")
    print(f"🔎 Confidence: {confidence:.2f}")
    #print(f"📄 Input: {text[:100]}...")


if __name__ == "__main__":
    test_cases = [
        # --- STRONG FAKE ---
        """
BREAKING: Massive scam uncovered as documents show high-level corruption in the allocation of COVID relief funds!!! Anonymous sources claim that key officials were involved in redirecting billions into offshore accounts. This comes just weeks before elections, raising serious questions. SHOCKING footage leaked online shows alleged evidence — and the government has made no official statement yet. Stay tuned for updates!!!
""", 
"""According to multiple unnamed insiders, the recent move by the finance ministry to fast-track disinvestment in public sector undertakings may not be purely economical. Observers have noted that the announcement, which came late on a Friday evening, closely followed a high-profile political meeting — prompting speculation that the decision may serve dual purposes. While no evidence currently supports this theory, the timing has raised eyebrows among analysts.
""", 
"""The Ministry of Finance on Friday announced the disinvestment of two public sector companies as part of its broader economic reform agenda. In an official press release, the ministry stated that the move is aimed at enhancing efficiency, encouraging private participation, and reducing fiscal burden. The announcement follows similar actions taken earlier in the fiscal year and is expected to contribute to the government’s target of ₹1.75 lakh crore in disinvestment revenue for FY2025.
""", 
"""BREAKING NEWS: Shocking incident from Delhi High Court!! Huge amount of cash was found at Justice Varma's house according to reports and many peoples are saying this is not just coincidence. Some insiders claim that this could be something massive going on behind closed doors!!
Union Law Minister Arjun Ram Meghwal told this to ANI, saying that the issue is being handled by Supreme Court now. He said, "Let the committee report come then we will say anything else" and he didn't give clear answers. This is making people more curious what is happening.
Burnt 500 rupee notes were seen by cleaning workers outside the house and they said they saw it that day only, and nobody is knowing where fire even came from. "We found it. It was there. We don’t know anything else", one worker said.
Meanwhile, a 3-judge panel has been formed but many believe that this could be bigger than just a case of some money. Some media reports said that fire tenders reached there and found cash in strange place — not even in main house, but in some outhouse. This is suspicious.
Justice Varma denied all things and said it's a conspiracy to defame and frame him. But people are asking, if nothing is wrong then how come money was found? Some even believe that data on his phone could give more clue — and reports say the Chief Justice asked him to save his messages and calls.
At the same time, Law Minister Meghwal was in Manipur for another event but he also said something about Manipur future after President Rule — again not much detail. All this happening at once... and people are wondering what is truth behind it???
STAY TUNED for more updates!!
""", 
"""BREAKING NEWS:Cash found at Justice Varma residence: ‘Let committee report come’, says Arjun Ram Meghwal
Union Law Minister addresses Delhi High Court judge’s cash row controversy, Supreme Court forms committee
Published - March 24, 2025 07:52 am IST - Imphal, Manipur
PTI
The Supreme Court also released the response of Justice Yashwant Varma, who has denied the allegations and said that it clearly appeared to be a conspiracy to frame and malign him.  File
The Supreme Court also released the response of Justice Yashwant Varma, who has denied the allegations and said that it clearly appeared to be a conspiracy to frame and malign him.  File | Photo Credit: X/@arjunrammeghwal via PTI Photo
Union Law Minister Arjun Ram Meghwal on Sunday (March 23, 2025) addressed the controversy surrounding Delhi High Court judge Justice Yashwant Varma, who is facing a probe over cash allegedly recovered from his residence!!!
He clarified that the matter is currently with the Supreme Court, which has constituted a three-member committee to investigate the issue. “This case is with the Supreme Court. It has formed a three-member committee including two High Court Chief Justices and one High Court Judge. Let the committee report come. Then we will talk about this...,” Mr. Meghwal told ANI in Imphal.
Notably, sanitation workers have said they found burnt pieces of currency notes near the official residence of Delhi High Court judge Justice Yashwant Varma who is facing a probe over cash allegedly recovered from his residence. “We work in this circle. We collect garbage from the roads. We were cleaning here 4-5 days back and collecting garbage when we found some small pieces of burnt ₹500 note. We found it that day. Now, we have found 1-2 pieces...We do not know where a fire broke out,” Inderjeet, a sanitation worker, told ANI.
No cash kept in storeroom either by me or my family members: Delhi High Court Judge Varma
Meanwhile, Chief Justice of India Sanjiv Khanna on Saturday (March 22, 2025) constituted a three-member committee consisting of Punjab and Haryana High Court Chief Justice Sheel Nagu, Himachal Pradesh Chief Justice G.S. Sandhawalia and Karnataka High Court Judge, Justice Anu Sivaraman to conduct an inquiry into the allegations.
The Supreme Court has released the inquiry report filed by Delhi High Court Chief Justice Devendra Kumar Upadhyay into the controversy involving High Court Justice Yashwant Varma, as per a press release by the Supreme Court.
In his report, the Delhi High Court Chief Justice said that he is of the prima facie opinion that the entire matter warrants a deeper probe.
The Supreme Court also released the response of Justice Yashwant Varma, who has denied the allegations and said that it clearly appeared to be a conspiracy to frame and malign him.
Justice Varma stated that no cash was ever placed in that storeroom either by him or any of his family members, and he said he strongly denounced the suggestion that the alleged cash belonged to them. The room which caught fire and where cash was allegedly found was an outhouse and not the main building where the judge and family reside, he stated.
The Chief Justice of the Delhi High Court, Devendra Kumar Upadhyay, instructed Justice Yashwant Varma to preserve all communication on his phone while acting on the directive of the Chief Justice of India (CJI); this included conversations, messages, and data, as the controversy surrounding him continued to unfold. Justice Varma, in a statement to Delhi High Court Chief Justice Devendra Kumar Upadhyay, refuted the allegations implicating him in the cash recovery incident.
"""
    ]

    a = 0
    for text in test_cases:
        a+=1
        #print(a)
        predict(text)
