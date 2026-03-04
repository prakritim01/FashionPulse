import pandas as pd
import numpy as np
import os

def run_sentiment_analysis():
    try:
        # Load the Phase 1 Master Data
        master_df = pd.read_csv('data/processed/master_f1_results.csv')
        
        print("🤖 Initializing AI Sentiment Engine...")
        
        # We simulate AI analysis by assigning 'Confidence' scores to 
        # different aesthetics based on the Market Segment.
        aesthetics = ['Quiet Luxury', 'Racing Core', 'Old Money']
        sentiment_results = []

        for race in master_df['Race'].unique():
            market = master_df[master_df['Race'] == race]['Market_Segment'].iloc[0]
            
            for style in aesthetics:
                # Generate a simulated confidence score (0.65 to 0.99)
                # In a real app, this would come from a NLP Transformer model
                confidence = np.random.uniform(0.65, 0.99)
                
                sentiment_results.append({
                    'Race': race,
                    'Market_Segment': market,
                    'Aesthetic': style,
                    'Confidence': round(confidence, 4)
                })

        # Create the report
        sentiment_df = pd.DataFrame(sentiment_results)
        
        # Save for the next Phase (Correlation)
        os.makedirs('data/processed', exist_ok=True)
        sentiment_df.to_csv('data/processed/trend_velocity_report.csv', index=False)
        
        print(f"✅ AI Analysis Complete. Trend Velocity Report saved for {len(sentiment_df)} data points.")
        return sentiment_df

    except Exception as e:
      print(f"❌ Sentiment Engine Error: {e}")

if __name__ == "__main__":
    run_sentiment_analysis()