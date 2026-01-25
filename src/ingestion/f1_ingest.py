import fastf1
import pandas as pd
import os

# Create a cache directory to avoid repeated heavy downloads
CACHE_DIR = 'data/cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR, exist_ok=True)

# Enabling cache is standard practice in F1 data science
fastf1.Cache.enable_cache(CACHE_DIR)

def fetch_race_data(year, gp_name):
    """
    Ingests F1 race results for a specific year and Grand Prix.
    This serves as the foundation for our FashionPulse correlation model.
    """
    try:
        print(f"🏎️  Loading {year} {gp_name} Grand Prix...")
        session = fastf1.get_session(year, gp_name, 'R')
        session.load(telemetry=False, weather=False)
        
        # We only need the top finishers and team names for sentiment correlation
        results = session.results[['Abbreviation', 'TeamName', 'FullName', 'ClassifiedPosition']]
        
        # Filter for top 10 (Points scorers usually drive the most sentiment)
        top_10 = results.head(10)
        
        print(f"✅ Successfully fetched data for {gp_name}")
        return top_10
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return None

if __name__ == "__main__":
    # Test with the Monaco GP (The high-fashion capital of F1)
    df = fetch_race_data(2025, 'Monaco')
    if df is not None:
        print("\n--- Top 10 Finishers ---")
        print(df)
        
        # Save to processed data folder
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv('data/processed/monaco_2025_results.csv', index=False)
        print("\n💾 Data saved to data/processed/monaco_2025_results.csv")