import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import fastf1
import joblib
import os
import glob
import warnings

# Suppress warnings for cleaner terminal output
warnings.simplefilter(action='ignore', category=FutureWarning)
fastf1.Cache.enable_cache('data/cache')

def train_podium_predictor():
    print("🏆 Initializing Podium Predictor ML Model...")
    
    # 1. Load the engineered pace features
    feature_files = glob.glob('data/processed/features/race_features_*.csv')
    if not feature_files:
        print("❌ No race features found. Run Phase 2 first.")
        return
        
    df_list = [pd.read_csv(f) for f in feature_files]
    features_df = pd.concat(df_list, ignore_index=True)
    
    # 2. Dynamically fetch the target labels (Actual Finishing Positions) from the cache
    print("🔄 Matching features with actual race outcomes...")
    results_list = []
    for (year, round_num), group in features_df.groupby(['Year', 'Round']):
        session = fastf1.get_session(year, round_num, 'R')
        session.load(telemetry=False, weather=False, messages=False)
        
        res = session.results[['Abbreviation', 'Position']].copy()
        res['Year'] = year
        res['Round'] = round_num
        results_list.append(res)
        
    targets_df = pd.concat(results_list, ignore_index=True)
    targets_df = targets_df.rename(columns={'Abbreviation': 'Driver'})
    
    # 3. Merge features with their actual targets
    data = pd.merge(features_df, targets_df, on=['Year', 'Round', 'Driver'], how='inner')
    
    # Clean the dataset
    data = data.dropna(subset=['AvgPace', 'PaceConsistency', 'Position'])
    
    # 4. Define the Target Variable: 1 if Podium (Top 3), else 0
    data['Podium'] = (data['Position'] <= 3).astype(int)
    
    # Define the input features
    feature_cols = ['AvgPace', 'FastestLap', 'PaceConsistency']
    X = data[feature_cols]
    y = data['Podium']
    
    if len(data) < 10:
        print("⚠️ Warning: Very small dataset. Training anyway to validate the pipeline.")
        
    # 5. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 6. Train the LightGBM Classifier
    print("🚀 Training LightGBM Classifier...")
    model = lgb.LGBMClassifier(
        n_estimators=100, 
        learning_rate=0.05, 
        random_state=42,
        verbose=-1 # Suppress LightGBM internal logs
    )
    model.fit(X_train, y_train)
    
    # 7. Evaluate Accuracy
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"📊 Model Evaluation - Classification Accuracy: {acc*100:.2f}%")
    
    # 8. Save Model to Registry
    os.makedirs('models_registry', exist_ok=True)
    joblib.dump(model, 'models_registry/podium_model.pkl')
    joblib.dump(feature_cols, 'models_registry/podium_model_features.pkl')
    print("✅ Podium Predictor Model saved to models_registry/podium_model.pkl")

if __name__ == "__main__":
    train_podium_predictor()