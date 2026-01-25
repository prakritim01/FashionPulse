from transformers import pipeline
import pandas as pd
import os

def analyze_fashion_sentiment(text_list):
    """
    Uses a DistilBERT model to analyze sentiment of fashion-related text.
    """
    # This downloads the model on the first run (~250MB)
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return classifier(text_list)

if __name__ == "__main__":
    fashion_comments = [
        "Charles Leclerc wearing custom Giorgio Armani in the paddock is pure quiet luxury.",
        "The Ferrari red this weekend is absolutely iconic, best paddock style so far!",
        "Monaco fashion is getting a bit boring, too much of the same old money look.",
        "Lando Norris's victory kit is a bit loud for my taste, not very chic."
    ]
    
    print("🧠 Analyzing Fashion Sentiment...")
    sentiments = analyze_fashion_sentiment(fashion_comments)
    
    df = pd.DataFrame({
        'Comment': fashion_comments,
        'Sentiment': [res['label'] for res in sentiments],
        'Confidence': [round(res['score'], 4) for res in sentiments]
    })
    
    print("\n--- Sentiment Analysis Results ---")
    print(df)
    
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/fashion_sentiment_sample.csv', index=False)
    print("\n💾 Results saved to data/processed/fashion_sentiment_sample.csv")