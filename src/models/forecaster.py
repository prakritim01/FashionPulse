import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

def generate_trend_forecasts():
    try:
        # Load the AI Sentiment data from Phase 2
        df = pd.read_csv('data/processed/trend_velocity_report.csv')
        
        print("🔮 Initializing AI Forecasting Hub...")
        
        forecast_results = []
        
        # We forecast the next 3 points for each unique aesthetic
        for style in df['Aesthetic'].unique():
            subset = df[df['Aesthetic'] == style].copy()
            
            # Prepare data: X is the sequence of races, y is the confidence
            X = np.array(range(len(subset))).reshape(-1, 1)
            y = subset['Confidence'].values
            
            # Simple Linear Regression for trend projection
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict for the next 3 future sessions
            future_steps = np.array(range(len(subset), len(subset) + 3)).reshape(-1, 1)
            predictions = model.predict(future_steps)
            
            for i, pred in enumerate(predictions):
                forecast_results.append({
                    'Race': f'Future Race +{i+1}',
                    'Aesthetic': style,
                    'Confidence': round(max(0, min(1, pred)), 4), # Keep score between 0 and 1
                    'Data_Type': 'Forecast'
                })

        # Combine with original data to show a full timeline
        forecast_df = pd.DataFrame(forecast_results)
        
        os.makedirs('data/processed', exist_ok=True)
        forecast_df.to_csv('data/processed/trend_forecast.csv', index=False)
        
        print(f"✅ Forecasting Complete. {len(forecast_df)} future data points projected.")
        return forecast_df

    except Exception as e:
        print(f"❌ Forecasting Error: {e}")

if __name__ == "__main__":
    generate_trend_forecasts()