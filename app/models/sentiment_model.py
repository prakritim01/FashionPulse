import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
import os
from datetime import datetime

def analyze_f1_sentiment():
    print("📰 Initializing F1 Sentiment & Momentum Analyzer...")
    
    # 1. Fetch live F1 news from a public RSS feed (Motorsport.com)
    rss_url = "https://www.motorsport.com/rss/f1/news/"
    
    try:
        # Use a standard browser header to ensure the feed provider doesn't block us
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the XML feed
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            desc = item.find('description').text if item.find('description') is not None else ""
            articles.append((title + " " + desc).lower())
            
        print(f"📡 Successfully downloaded {len(articles)} recent F1 news articles.")
        
    except Exception as e:
        print(f"⚠️ Could not fetch live RSS feed ({e}). Using mock recent headlines for pipeline testing.")
        articles = [
            "norris secures brilliant pole position with new mclaren upgrade",
            "verstappen engine penalty causes massive struggle in qualifying",
            "leclerc crash in fp2 brings out red flag, ferrari analyzing damage",
            "hamilton praises mercedes pace, confident for podium finish",
            "piastri extends contract after strong dominate masterclass performance",
            "sainz out with engine failure, disastrous weekend for the spaniard"
        ]

    # 2. Define the Grid (Drivers to track)
    drivers = [
        "verstappen", "norris", "leclerc", "hamilton", "sainz", 
        "piastri", "russell", "perez", "alonso", "stroll", 
        "gasly", "ocon", "albon", "colapinto", "tsunoda", 
        "hulkenberg", "magnussen", "bottas", "zhou", "lawson"
    ]

    # 3. Define the F1 Custom Lexicon
    # We assign weights to specific words. A generic sentiment analyzer wouldn't 
    # know that "pole" is good and "red flag" is bad. Ours does.
    lexicon = {
        # Positive Momentum
        "win": 3, "pole": 3, "podium": 2, "upgrade": 2, "fast": 1, 
        "quick": 1, "strong": 1, "dominate": 3, "masterclass": 3, 
        "extends": 2, "champion": 3, "brilliant": 2, "smooth": 1, "confident": 2,
        # Negative Momentum
        "crash": -3, "dnf": -3, "penalty": -3, "struggle": -2, "slow": -1, 
        "spin": -2, "fire": -3, "issue": -2, "failure": -3, "retire": -3, 
        "out": -2, "complain": -1, "worse": -1, "investigation": -2, "damage": -2
    }

    print("🧠 Processing NLP Lexicon Scoring...")
    
    # 4. Score the drivers
    driver_scores = {driver: 0 for driver in drivers}
    driver_mentions = {driver: 0 for driver in drivers}

    for article in articles:
        # Strip out special characters for clean word matching
        clean_text = re.sub(r'[^\w\s]', '', article)
        words = clean_text.split()
        
        # Check which drivers are mentioned in this article
        mentioned_drivers = [d for d in drivers if d in words]
        
        if mentioned_drivers:
            # Calculate the sentiment score of the article
            article_score = 0
            for word in words:
                if word in lexicon:
                    article_score += lexicon[word]
            
            # Attribute the score to the drivers mentioned
            for driver in mentioned_drivers:
                driver_scores[driver] += article_score
                driver_mentions[driver] += 1

    # 5. Format and normalize the results
    results = []
    for driver in drivers:
        mentions = driver_mentions[driver]
        raw_score = driver_scores[driver]
        # Calculate average sentiment per mention (avoiding divide-by-zero)
        avg_sentiment = (raw_score / mentions) if mentions > 0 else 0
        
        results.append({
            'Driver': driver.title(),
            'Mentions': mentions,
            'Total_Sentiment_Score': raw_score,
            'Momentum_Index': round(avg_sentiment, 2),
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    df_sentiment = pd.DataFrame(results)
    
    # Sort by Momentum Index (Hottest drivers at the top)
    df_sentiment = df_sentiment.sort_values(by='Momentum_Index', ascending=False)
    
    # 6. Save the intelligence report
    os.makedirs('data/processed/reports', exist_ok=True)
    report_path = 'data/processed/reports/live_sentiment.csv'
    df_sentiment.to_csv(report_path, index=False)
    
    print(f"✅ Sentiment Intelligence Engine complete. Report saved to {report_path}")
    
    # Display the top 3 drivers with the most positive momentum right now
    print("\n📈 Current F1 Media Momentum (Top 3):")
    top_3 = df_sentiment[df_sentiment['Mentions'] > 0].head(3)
    if not top_3.empty:
        for _, row in top_3.iterrows():
            print(f"  🏎️ {row['Driver']}: {row['Momentum_Index']} Index ({row['Mentions']} Mentions)")
    else:
        print("  No significant momentum detected in current news cycle.")

if __name__ == "__main__":
    analyze_f1_sentiment()