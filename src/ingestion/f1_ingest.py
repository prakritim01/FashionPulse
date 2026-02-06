import fastf1
import pandas as pd
import os

# Enabling cache for the global dataset
CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

# 2025 Global Calendar: Stable data for the Enterprise Hub
RACES = [
    {'year': 2025, 'location': 'Shanghai', 'market': 'Asian High-Fashion'},
    {'year': 2025, 'location': 'Miami', 'market': 'US Streetwear'},
    {'year': 2025, 'location': 'Monaco', 'market': 'European Luxury'},
    {'year': 2025, 'location': 'Silverstone', 'market': 'British Heritage'},
    {'year': 2025, 'location': 'Singapore', 'market': 'Asian Tech-Luxe'},
    {'year': 2025, 'location': 'Las Vegas', 'market': 'Premium Entertainment'},
    {'year': 2025, 'location': 'Abu Dhabi', 'market': 'High-End Exclusive'}
]

def ingest_enterprise_season():
    all_results = []
    for race in RACES:
        try:
            print(f"🏎️  Ingesting {race['location']} {race['year']}...")
            session = fastf1.get_session(race['year'], race['location'], 'R')
            session.load(telemetry=False, weather=False)
            
            results = session.results[['Abbreviation', 'TeamName', 'ClassifiedPosition']]
            results['Race'] = race['location']
            results['Market'] = race['market']
            
            all_results.append(results.head(10))
            print(f"✅ Market Data Added: {race['location']}")
            
        except Exception as e:
            print(f"❌ Failed {race['location']}: {e}")
    
    if all_results:
        master_df = pd.concat(all_results, ignore_index=True)
        os.makedirs('data/processed', exist_ok=True)
        master_df.to_csv('data/processed/master_f1_results.csv', index=False)
        print(f"\n💾 Enterprise Master Data saved! Total rows: {len(master_df)}")
        return master_df

if __name__ == "__main__":
    ingest_enterprise_season()