import fastf1
import pandas as pd
import os

# Create a cache directory to avoid repeated heavy downloads
CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

# Defining Phase 2 Race List: High-fashion hubs for 2025
RACES = [
    {'year': 2025, 'location': 'Monaco'},
    {'year': 2025, 'location': 'Miami'},
    {'year': 2025, 'location': 'Las Vegas'}
]

def ingest_multiple_races():
    """
    Ingests F1 results for multiple GPs to build a master dataset 
    for Phase 2 trend velocity analysis.
    """
    all_results = []
    
    for race in RACES:
        try:
            print(f"🏎️  Fetching data for {race['location']} {race['year']}...")
            session = fastf1.get_session(race['year'], race['location'], 'R')
            session.load(telemetry=False, weather=False)
            
            # Extracting core data for sentiment correlation
            results = session.results[['Abbreviation', 'TeamName', 'ClassifiedPosition']]
            
            # Labeling the data by race location for later grouping
            results['Race'] = race['location']
            results['Year'] = race['year']
            
            all_results.append(results.head(10)) # Top 10 scorers
            print(f"✅ Successfully added {race['location']}")
            
        except Exception as e:
            print(f"❌ Failed to fetch {race['location']}: {e}")
    
    if all_results:
        # Create a Master Dataframe combining all races
        master_df = pd.concat(all_results, ignore_index=True)
        
        # Save to processed data folder
        os.makedirs('data/processed', exist_ok=True)
        master_df.to_csv('data/processed/master_f1_results.csv', index=False)
        print(f"\n💾 Phase 2 Master Data saved! Total rows: {len(master_df)}")
        return master_df
    return None

if __name__ == "__main__":
    df = ingest_multiple_races()
    if df is not None:
        print("\n--- Phase 2 Master Data Preview ---")
        print(df.head())