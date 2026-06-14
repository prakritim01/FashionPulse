import fastf1
import pandas as pd
import os

# Enable FastF1 caching to avoid re-downloading large telemetry files
CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def load_weather_data(year):
    print(f"☁️ Starting Weather Ingestion for {year} Season...")
    schedule = fastf1.get_event_schedule(year)
    all_weather = []
    
    for _, event in schedule.iterrows():
        # Skip testing events and future races
        if event['EventFormat'] == 'testing' or event['EventDate'] > pd.Timestamp.now():
            continue
            
        try:
            print(f"📡 Fetching weather for: {event['EventName']}...")
            session = fastf1.get_session(year, event['RoundNumber'], 'R')
            
            # We ONLY load weather here to speed up execution
            session.load(telemetry=False, laps=False, messages=False, weather=True)
            
            weather_df = session.weather_data.copy()
            weather_df['Race'] = event['EventName']
            weather_df['Round'] = event['RoundNumber']
            weather_df['Year'] = year
            
            all_weather.append(weather_df)
            print(f"✅ Weather for {event['EventName']} processed.")
            
        except Exception as e:
            print(f"❌ Error processing weather for {event['EventName']}: {e}")
            continue
            
    if all_weather:
        master_df = pd.concat(all_weather, ignore_index=True)
        os.makedirs('data/raw/weather', exist_ok=True)
        filename = f'data/raw/weather/weather_{year}.csv'
        master_df.to_csv(filename, index=False)
        print(f"💾 Season {year} weather saved successfully to {filename}")
    else:
        print(f"⚠️ No weather data found for {year}.")

if __name__ == "__main__":
    # Test by fetching the 2024 season
    load_weather_data(2024)