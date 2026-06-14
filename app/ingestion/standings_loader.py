import fastf1
import pandas as pd
import os

CACHE_DIR = 'data/cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def calculate_standings(year):
    print(f"🛠️ Engineering {year} Standings directly from raw session logs...")
    schedule = fastf1.get_event_schedule(year)
    
    all_points = []
    
    for _, event in schedule.iterrows():
        # Skip testing and future dates
        if event['EventFormat'] == 'testing' or event['EventDate'] > pd.Timestamp.now():
            continue
            
        print(f"📊 Aggregating points for: {event['EventName']}")
        
        # 1. Extract Race Points
        try:
            race = fastf1.get_session(year, event['RoundNumber'], 'Race')
            # Load minimal data to keep it lightning fast
            race.load(telemetry=False, weather=False, messages=False)
            if not race.results.empty:
                df_race = race.results[['FullName', 'DriverNumber', 'TeamName', 'Points', 'Position']].copy()
                df_race['Type'] = 'Race'
                all_points.append(df_race)
        except Exception as e:
            print(f"  - No race data for round {event['RoundNumber']}")
            
        # 2. Extract Sprint Points (if the weekend format includes a sprint)
        if event['EventFormat'] in ['sprint_format', 'sprint', 'sprint_shootout']:
            try:
                sprint = fastf1.get_session(year, event['RoundNumber'], 'Sprint')
                sprint.load(telemetry=False, weather=False, messages=False)
                if not sprint.results.empty:
                    df_sprint = sprint.results[['FullName', 'DriverNumber', 'TeamName', 'Points', 'Position']].copy()
                    df_sprint['Type'] = 'Sprint'
                    all_points.append(df_sprint)
            except Exception as e:
                print(f"  - No sprint data for round {event['RoundNumber']}")

    if not all_points:
        print("⚠️ No session data found.")
        return

    # Combine every session of the year into one master dataframe
    master_df = pd.concat(all_points, ignore_index=True)
    os.makedirs('data/raw/races', exist_ok=True)
    
    # --- 1. Engineer Driver Standings ---
    # Group by driver and sum their points
    driver_st = master_df.groupby(['FullName', 'DriverNumber', 'TeamName'])['Points'].sum().reset_index()
    driver_st = driver_st.sort_values(by='Points', ascending=False).reset_index(drop=True)
    
    # Calculate Race Wins (Position 1 in a 'Race')
    wins = master_df[(master_df['Type'] == 'Race') & (master_df['Position'] == 1.0)].groupby('FullName').size().reset_index(name='Wins')
    
    # Merge and format
    driver_st = pd.merge(driver_st, wins, on='FullName', how='left')
    driver_st['Wins'] = driver_st['Wins'].fillna(0).astype(int)
    driver_st['Position'] = driver_st.index + 1
    driver_st['Year'] = year
    
    driver_st = driver_st.rename(columns={'FullName': 'Driver', 'DriverNumber': 'DriverId', 'TeamName': 'Constructor'})
    driver_st.to_csv(f'data/raw/races/driver_standings_{year}.csv', index=False)
    print(f"✅ Driver standings for {year} mathematically engineered and saved.")
    
    # --- 2. Engineer Constructor Standings ---
    # Group by team and sum points
    constructor_st = master_df.groupby('TeamName')['Points'].sum().reset_index()
    constructor_st = constructor_st.sort_values(by='Points', ascending=False).reset_index(drop=True)
    
    # Calculate Team Wins
    constructor_st['Wins'] = constructor_st['TeamName'].map(
        master_df[(master_df['Type'] == 'Race') & (master_df['Position'] == 1.0)].groupby('TeamName').size()
    ).fillna(0).astype(int)
    
    # Format
    constructor_st['Position'] = constructor_st.index + 1
    constructor_st['Year'] = year
    constructor_st['ConstructorId'] = constructor_st['TeamName'].str.lower().str.replace(' ', '_')
    constructor_st = constructor_st.rename(columns={'TeamName': 'Constructor'})
    
    constructor_st.to_csv(f'data/raw/races/constructor_standings_{year}.csv', index=False)
    print(f"✅ Constructor standings for {year} mathematically engineered and saved.")

if __name__ == "__main__":
    calculate_standings(2024)