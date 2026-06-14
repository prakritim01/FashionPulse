import fastf1
import pandas as pd
import numpy as np
import os

# Use the established cache to speed up loading
CACHE_DIR = 'data/cache'
fastf1.Cache.enable_cache(CACHE_DIR)

def generate_driver_features(year, round_num):
    print(f"⚙️ Engineering pace features for {year} Round {round_num}...")
    try:
        session = fastf1.get_session(year, round_num, 'R')
        session.load(telemetry=False, weather=False)
        
        laps = session.laps
        features = []
        
        for driver in session.results['Abbreviation']:
            # Pick laps for the driver under green flag conditions (TrackStatus '1')
            driver_laps = laps.pick_driver(driver).pick_track_status('1')
            if driver_laps.empty:
                continue
            
            # Convert lap time to total seconds for mathematical operations
            lap_times = driver_laps['LapTime'].dt.total_seconds().dropna()
            
            if len(lap_times) > 0:
                avg_pace = lap_times.mean()
                fastest_lap = lap_times.min()
                consistency = lap_times.std() # Lower = more consistent
            else:
                avg_pace, fastest_lap, consistency = np.nan, np.nan, np.nan
                
            features.append({
                'Year': year,
                'Round': round_num,
                'Driver': driver,
                'AvgPace': avg_pace,
                'FastestLap': fastest_lap,
                'PaceConsistency': consistency,
                'ValidLaps': len(lap_times)
            })
            
        df_features = pd.DataFrame(features)
        
        os.makedirs('data/processed/features', exist_ok=True)
        filename = f'data/processed/features/race_features_{year}_{round_num}.csv'
        df_features.to_csv(filename, index=False)
        print(f"✅ Features saved to {filename}")
        return df_features
        
    except Exception as e:
        print(f"❌ Error generating features: {e}")
        return None

if __name__ == "__main__":
    # Test by processing 2024 Round 1 (Bahrain)
    generate_driver_features(2024, 1)