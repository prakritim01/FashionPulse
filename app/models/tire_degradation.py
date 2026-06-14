import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os
import glob
import warnings

# Suppress pandas FutureWarnings for cleaner output
warnings.simplefilter(action='ignore', category=FutureWarning)

def train_tire_degradation_model():
    print("🧠 Initializing Tire Degradation ML Model...")
    
    # 1. Load all available tire features dynamically
    feature_files = glob.glob('data/processed/features/tire_features_*.csv')
    if not feature_files:
        print("❌ No tire features found. Run Phase 2 first.")
        return
        
    df_list = [pd.read_csv(f) for f in feature_files]
    data = pd.concat(df_list, ignore_index=True)
    
    # 2. Clean and Prepare Data
    # Drop rows where DegradationRate is missing or infinite
    data = data.dropna(subset=['DegradationRate', 'Compound', 'StintLength'])
    
    # One-hot encode the tire compounds (SOFT, MEDIUM, HARD, INTERMEDIATE, WET)
    data = pd.get_dummies(data, columns=['Compound'])
    
    # Define our inputs (X) and what we want to predict (y)
    features = [col for col in data.columns if col.startswith('Compound_')] + ['StintLength']
    X = data[features]
    y = data['DegradationRate']
    
    if len(data) < 10:
        print("⚠️ Warning: Very small dataset. The model will train, but feed it more races for accuracy!")
        
    # 3. Train/Test Split (80% training, 20% validation)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train XGBoost Regressor
    print("🚀 Training XGBoost Regressor on Stint Data...")
    model = xgb.XGBRegressor(
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5, 
        random_state=42,
        objective='reg:squarederror'
    )
    model.fit(X_train, y_train)
    
    # 5. Evaluate Accuracy
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"📊 Model Evaluation - Mean Absolute Error (MAE): {mae:.4f} seconds/lap")
    
    # 6. Save Model to Registry
    os.makedirs('models_registry', exist_ok=True)
    joblib.dump(model, 'models_registry/tire_model.pkl')
    
    # We also save the exact feature columns so our FastAPI layer knows what to expect later
    joblib.dump(features, 'models_registry/tire_model_features.pkl')
    print("✅ Tire Degradation Model saved to models_registry/tire_model.pkl")

if __name__ == "__main__":
    train_tire_degradation_model()