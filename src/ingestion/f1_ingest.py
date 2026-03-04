import fastf1
import pandas as pd
import os

# Set up professional caching to speed up repeated runs
CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

# Updated RACES list to use 2024 data for stability
# These locations represent diverse consumer segments
RACES = [
    # Asia & Middle East
    {'year': 2024, 'location': 'Shanghai', 'market': 'Asian Avant-Garde', 'lat': 31.3389, 'lon': 121.2203},
    {'year': 2024, 'location': 'Suzuka', 'market': 'Heritage Tech', 'lat': 34.8431, 'lon': 136.541},
    {'year': 2024, 'location': 'Sakhir', 'market': 'Middle-Eastern Opulence', 'lat': 26.0325, 'lon': 50.5106},
    {'year': 2024, 'location': 'Jeddah', 'market': 'Modern Desert Luxury', 'lat': 21.6319, 'lon': 39.1044},
    {'year': 2024, 'location': 'Singapore', 'market': 'Modern Urban Luxury', 'lat': 1.2915, 'lon': 103.8639},
    {'year': 2024, 'location': 'Baku', 'market': 'Caspian Chic', 'lat': 40.3725, 'lon': 49.8533},
    {'year': 2024, 'location': 'Lusail', 'market': 'Futuristic Elite', 'lat': 25.4900, 'lon': 51.4542},
    {'year': 2024, 'location': 'Yas Marina', 'market': 'Oasis Glamour', 'lat': 24.4672, 'lon': 54.6031},
    
    # Europe
    {'year': 2024, 'location': 'Monaco', 'market': 'Ultra-Luxury', 'lat': 43.7347, 'lon': 7.4206},
    {'year': 2024, 'location': 'Barcelona', 'market': 'Mediterranean Style', 'lat': 41.57, 'lon': 2.2611},
    {'year': 2024, 'location': 'Spielberg', 'market': 'Alpine Premium', 'lat': 47.2197, 'lon': 14.7647},
    {'year': 2024, 'location': 'Silverstone', 'market': 'British Racing Green', 'lat': 52.0786, 'lon': -1.0169},
    {'year': 2024, 'location': 'Spa', 'market': 'Forest Heritage', 'lat': 50.4372, 'lon': 5.9714},
    {'year': 2024, 'location': 'Budapest', 'market': 'Danube Elegance', 'lat': 47.583, 'lon': 19.248},
    {'year': 2024, 'location': 'Zandvoort', 'market': 'Coastal Casual', 'lat': 52.3888, 'lon': 4.5409},
    {'year': 2024, 'location': 'Monza', 'market': 'European Heritage', 'lat': 45.6189, 'lon': 9.2811},
    {'year': 2024, 'location': 'Imola', 'market': 'Motor Valley Luxury', 'lat': 44.3439, 'lon': 11.7167},
    
    # Americas
    {'year': 2024, 'location': 'Miami', 'market': 'High-End Streetwear', 'lat': 25.9581, 'lon': -80.2389},
    {'year': 2024, 'location': 'Montreal', 'market': 'Francophone Chic', 'lat': 45.5000, 'lon': -73.5228},
    {'year': 2024, 'location': 'Austin', 'market': 'Western Premium', 'lat': 30.1328, 'lon': -97.6411},
    {'year': 2024, 'location': 'Mexico City', 'market': 'Latam Vibrancy', 'lat': 19.4042, 'lon': -99.0907},
    {'year': 2024, 'location': 'Interlagos', 'market': 'Samba Luxury', 'lat': -23.7036, 'lon': -46.6997},
    {'year': 2024, 'location': 'Las Vegas', 'market': 'Premium Entertainment', 'lat': 36.1147, 'lon': -115.1728},
    
    # Oceania
    {'year': 2024, 'location': 'Melbourne', 'market': 'Pacific Lifestyle', 'lat': -37.8497, 'lon': 144.968}
]

def ingest_market_data():
    all_results = []
    print("🏎️ Starting Global Market Ingestion...")
    
    for race in RACES:
        try:
            print(f"📡 Fetching {race['location']} {race['year']}...")
            # Using FastF1 to get the session with a fallback strategy
            session = fastf1.get_session(race['year'], race['location'], 'R')
            session.load(telemetry=False, weather=False)
            
            results = session.results[['Abbreviation', 'TeamName', 'ClassifiedPosition']].head(10).copy()
            results['Race'] = race['location']
            results['Market_Segment'] = race['market']
            
            all_results.append(results)
            print(f"✅ {race['location']} Ingested.")
            
        except Exception as e:
            # If 2025 fails, we attempt 2024 for that specific race
            if race['year'] >= 2025:
                print(f"⚠️ {race['location']} {race['year']} failed. Retrying with 2024 data...")
                try:
                    session = fastf1.get_session(2024, race['location'], 'R')
                    session.load(telemetry=False, weather=False)
                    results = session.results[['Abbreviation', 'TeamName', 'ClassifiedPosition']].head(10).copy()
                    results['Race'] = race['location']
                    results['Market_Segment'] = race['market']
                    all_results.append(results)
                    print(f"✅ {race['location']} (2024 Fallback) Ingested.")
                    continue
                except:
                    pass
            print(f"❌ Error fetching {race['location']}: {e}")
            
    if all_results:
        master_df = pd.concat(all_results, ignore_index=True)
        os.makedirs('data/processed', exist_ok=True)
        master_df.to_csv('data/processed/master_f1_results.csv', index=False)
        print(f"\n💾 Phase 1 Complete. Master dataset saved: {len(master_df)} entries.")
        return master_df

if __name__ == "__main__":
    ingest_market_data()