from transformers import pipeline
import pandas as pd
import os

# Define our professional Aesthetic Keyword Mapping
AESTHETICS = {
    "Quiet Luxury": ["minimalist", "armani", "tailored", "neutral", "chic"],
    "Old Money": ["vintage", "heritage", "classic", "monaco", "linen", "aesthetic"],
    "Racing Chic": ["ferrari red", "streetwear", "paddock", "tag heuer", "merch"]
}

def classify_aesthetic(text):
    """
    Categorizes text into a fashion aesthetic based on keywords.
    """
    text = text.lower()
    for aesthetic, keywords in AESTHETICS.items():
        if any(word in text for word in keywords):
            return aesthetic
    return "General Fashion"

def analyze_fashion_sentiment(text_list):
    """
    Uses a DistilBERT model to analyze sentiment of fashion-related text.
    """
    # This downloads the model on the first run (~250MB)
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return classifier(text_list)

if __name__ == "__main__":
    # Sample data reflecting the Monaco GP fashion pulse
    fashion_comments = [
        "Charles Leclerc wearing custom Giorgio Armani in the paddock is pure quiet luxury.",
        "The Ferrari red this weekend is absolutely iconic, best paddock style so far!",
        "Monaco fashion is getting a bit boring, too much of the same old money look.",
        "Lando Norris's victory kit is a bit loud for my taste, not very chic."
    ]
    
    print("🧠 Analyzing Fashion Pulse (Sentiment + Aesthetics)...")
    
    # 1. Get Sentiment from AI Model
    sentiments = analyze_fashion_sentiment(fashion_comments)
    
    # 2. Get Aesthetic Tags from our Keyword Logic
    aesthetic_tags = [classify_aesthetic(comment) for comment in fashion_comments]
    
    # 3. Combine into a professional DataFrame
    df = pd.DataFrame({
        'Comment': fashion_comments,
        'Aesthetic': aesthetic_tags,
        'Sentiment': [res['label'] for res in sentiments],
        'Confidence': [round(res['score'], 4) for res in sentiments]
    })
    
    print("\n--- FashionPulse Integrated Analysis ---")
    print(df)
    
    # Save for the Dashboard and Correlation Engine
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/fashion_sentiment_sample.csv', index=False)
    print("\n💾 Results saved to data/processed/fashion_sentiment_sample.csv")