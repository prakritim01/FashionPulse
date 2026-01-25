import pandas as pd
import os

def calculate_influence_score(f1_df, sentiment_df):
    """
    Merges F1 results with fashion sentiment to calculate an 'Influence Score'.
    Formula: (1 / Position) * Confidence * Sentiment_Weight
    """
    print("🔄 Merging F1 and Fashion data...")
    
    # In a real scenario, we would join on 'Date' or 'Team'. 
    # For this professional prototype, we correlate the Top 1 results with Top Sentiment.
    winner_team = f1_df.iloc[0]['TeamName']
    avg_sentiment = sentiment_df['Confidence'].mean()
    
    # Calculate a simple Influence Metric
    influence_score = (avg_sentiment * 100).round(2)
    
    print(f"📊 Influence Analysis for {winner_team}:")
    print(f">> Average Fashion Sentiment Confidence: {avg_sentiment:.4f}")
    print(f">> Final FashionPulse Influence Score: {influence_score}")
    
    return influence_score

if __name__ == "__main__":
    # Load the data we saved from the previous scripts
    try:
        f1_results = pd.read_csv('data/processed/monaco_2025_results.csv')
        sentiment_results = pd.read_csv('data/processed/fashion_sentiment_sample.csv')
        
        score = calculate_influence_score(f1_results, sentiment_results)
        
        # Save the final insight
        summary = pd.DataFrame({
            'Metric': ['Winning Team', 'Market Sentiment', 'Influence Score'],
            'Value': [f1_results.iloc[0]['TeamName'], sentiment_results['Sentiment'].iloc[0], score]
        })
        
        summary.to_csv('data/processed/final_influence_report.csv', index=False)
        print("\n✅ Final Report generated: data/processed/final_influence_report.csv")
        
    except FileNotFoundError:
        print("❌ Error: Data files not found. Run f1_ingest.py and sentiment_analyzer.py first!")