import pandas as pd
import os

def calculate_influence_roi():
    try:
        # Load processed data from Phase 1 and Phase 2
        f1_results = pd.read_csv('data/processed/master_f1_results.csv')
        sentiment_trends = pd.read_csv('data/processed/trend_velocity_report.csv')

        print("💰 Initializing Correlation & ROI Engine...")

        # 1. Calculate a Performance Weight
        # Podium finishes (1-3) get the highest weight for brand influence
        def get_perf_weight(pos):
            if pos <= 3: return 1.5  # 50% boost for podiums
            if pos <= 10: return 1.0 # Standard Top 10 influence
            return 0.5               # Baseline for others
        
        f1_results['Perf_Weight'] = f1_results['ClassifiedPosition'].apply(get_perf_weight)

        # 2. Merge with AI Sentiment Data
        # We link the race results to the average confidence of aesthetics in that market
        avg_market_sentiment = sentiment_trends.groupby('Race')['Confidence'].mean().reset_index()
        combined_df = pd.merge(f1_results, avg_market_sentiment, on='Race')

        # 3. Calculate the Brand Influence Score (ROI)
        # Formula: Performance Weight * Market Confidence * 100 (Scale)
        combined_df['Influence_ROI'] = (combined_df['Perf_Weight'] * combined_df['Confidence'] * 100).round(2)

        # 4. Save the Enterprise ROI Report
        os.makedirs('data/processed', exist_ok=True)
        combined_df.to_csv('data/processed/brand_roi_report.csv', index=False)
        
        # Summary for the terminal
        top_team = combined_df.loc[combined_df['Influence_ROI'].idxmax()]
        print(f"✅ ROI Engine Complete.")
        print(f"📊 Top Influencer Identified: {top_team['TeamName']} at {top_team['Race']} (${top_team['Influence_ROI']}k Value)")
        
        return combined_df

    except Exception as e:
        print(f"❌ ROI Engine Error: {e}")

if __name__ == "__main__":
    calculate_influence_roi()