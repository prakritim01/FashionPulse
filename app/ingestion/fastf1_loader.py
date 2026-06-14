import fastf1
import pandas as pd
import os

# Professional caching setup
CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def ingest_season_data(year):
    print(f"🏎️ Starting Ingestion for {year} Season...")
    
    # Get the official FIA calendar for the year
    schedule = fastf1.get_event_schedule(year)
    all_results = []
    
    for _, event in schedule.iterrows():
        # Skip non-race events and future races
        if event['EventFormat'] == 'testing' or event['EventDate'] > pd.Timestamp.now():
            continue
            
        try:
            print(f"📡 Processing: {event['EventName']}...")
            session = fastf1.get_session(year, event['RoundNumber'], 'R')
            session.load(telemetry=False, weather=False)
            
            results = session.results.copy()
            # Ensure 'Race' is mapped so legacy ROI models still attach properly
            results['Race'] = event['EventName']
            results['EventName'] = event['EventName']
            results['Round'] = event['RoundNumber']
            results['Year'] = year
            
            # Select specific columns to ensure consistency across seasons
            cols_to_keep = ['Abbreviation', 'FullName', 'TeamName', 'ClassifiedPosition', 'Position', 'Points', 'Status', 'Race', 'EventName', 'Round', 'Year']
            
            # Use intersection to avoid KeyError if a column is missing in older years
            cols = [col for col in cols_to_keep if col in results.columns]
            results = results[cols]
            
            all_results.append(results)
            print(f"✅ {event['EventName']} processed.")
            
        except Exception as e:
            print(f"❌ Error processing {event['EventName']}: {e}")
            continue
            
    if all_results:
        master_df = pd.concat(all_results, ignore_index=True)
        os.makedirs('data/processed', exist_ok=True)
        filename = f'data/processed/f1_results_{year}.csv'
        master_df.to_csv(filename, index=False)
        print(f"💾 Season {year} data saved successfully to {filename}")
    else:
        print(f"⚠️ No results found for {year}.")

if __name__ == "__main__":
    ingest_season_data(2024)
    ingest_season_data(2025)
    ingest_season_data(2026)