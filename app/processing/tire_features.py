import fastf1
import pandas as pd
import os

CACHE_DIR = 'data/cache'
fastf1.Cache.enable_cache(CACHE_DIR)

def generate_tire_features(year, round_num):
    print(f"🛞 Engineering tire features for {year} Round {round_num}...")
    try:
        session = fastf1.get_session(year, round_num, 'R')
        session.load(telemetry=False, weather=False)
        laps = session.laps
        
        features = []
        
        for driver in session.results['Abbreviation']:
            driver_laps = laps.pick_driver(driver)
            
            # Group the driver's laps by stint
            for stint, stint_data in driver_laps.groupby('Stint'):
                if stint_data.empty:
                    continue
                    
                compound = stint_data['Compound'].iloc[0]
                stint_length = len(stint_data)
                
                # Calculate degradation by looking at the lap-over-lap drop in pace
                # We ignore the first and last lap of a stint (in/out laps) for clean data
                clean_laps = stint_data.iloc[1:-1]
                if len(clean_laps) > 3:
                    lap_times = clean_laps['LapTime'].dt.total_seconds()
                    # Calculate the average time lost per lap in seconds
                    degradation_rate = lap_times.diff().mean() 
                else:
                    degradation_rate = None
                    
                features.append({
                    'Year': year,
                    'Round': round_num,
                    'Driver': driver,
                    'Stint': stint,
                    'Compound': compound,
                    'StintLength': stint_length,
                    'DegradationRate': degradation_rate
                })
                
        df_tires = pd.DataFrame(features)
        os.makedirs('data/processed/features', exist_ok=True)
        filename = f'data/processed/features/tire_features_{year}_{round_num}.csv'
        df_tires.to_csv(filename, index=False)
        print(f"✅ Tire features saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error generating tire features: {e}")

if __name__ == "__main__":
    # Test by processing 2024 Round 1 (Bahrain)
    generate_tire_features(2024, 1)