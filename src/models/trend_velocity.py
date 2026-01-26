import pandas as pd
import os

def calculate_velocity(sentiment_df):
    """
    Calculates the 'Velocity' (Change in Sentiment) across different races.
    Formula: Velocity = (Current_Confidence - Previous_Confidence)
    """
    print("📈 Calculating Trend Velocity across the F1 Season...")
    
    # In a real-world scenario, we'd have thousands of rows. 
    # For our master prototype, we'll simulate the city-based trend shift.
    
    # Grouping by Aesthetic and Race to see the confidence average
    velocity_report = sentiment_df.groupby(['Race', 'Aesthetic'])['Confidence'].mean().reset_index()
    
    # Calculating the 'Shift' (Velocity)
    velocity_report['Velocity'] = velocity_report.groupby('Aesthetic')['Confidence'].diff().fillna(0)
    
    # Adding a 'Status' label
    velocity_report['Status'] = velocity_report['Velocity'].apply(
        lambda x: "🔥 Rising" if x > 0 else ("❄️ Falling" if x < 0 else "↔️ Stable")
    )
    
    return velocity_report

if __name__ == "__main__":
    # Load the master sentiment data
    # (Note: For the prototype, we use the sample data we've been building)
    try:
        sentiment_data = pd.read_csv('data/processed/fashion_sentiment_sample.csv')
        
        # Adding a mock 'Race' column for the velocity calculation
        # In the next step, we will automate this link!
        sentiment_data['Race'] = 'Monaco' 
        
        report = calculate_velocity(sentiment_data)
        
        print("\n--- Phase 2: Trend Velocity Report ---")
        print(report[['Race', 'Aesthetic', 'Confidence', 'Status']])
        
        os.makedirs('data/processed', exist_ok=True)
        report.to_csv('data/processed/trend_velocity_report.csv', index=False)
        print("\n💾 Velocity Report saved to data/processed/trend_velocity_report.csv")
        
    except FileNotFoundError:
        print("❌ Error: Run sentiment_analyzer.py first!")