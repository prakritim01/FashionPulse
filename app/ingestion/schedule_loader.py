import fastf1
import os

CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def load_schedule(year):
    print(f"📅 Fetching Schedule for {year}...")
    try:
        # Fetch the official FIA schedule via FastF1
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        
        os.makedirs('data/raw/races', exist_ok=True)
        filename = f'data/raw/races/schedule_{year}.csv'
        
        schedule.to_csv(filename, index=False)
        print(f"✅ Schedule for {year} saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error fetching schedule for {year}: {e}")

if __name__ == "__main__":
    load_schedule(2024)
    load_schedule(2025)