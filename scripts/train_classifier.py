import mlflow
import mlflow.lightgbm
import lightgbm as lgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
import os

# Ensure the model registry exists
os.makedirs('models_registry', exist_ok=True)

def generate_synthetic_f1_data(n_samples=5000):
    np.random.seed(42)
    avg_pace = np.random.uniform(80.0, 95.0, n_samples)
    fastest_lap = avg_pace - np.random.uniform(0.5, 2.5, n_samples)
    consistency = np.random.uniform(0.01, 0.15, n_samples)
    
    # Logic: Faster pace + high consistency = higher podium chance
    score = (95.0 - avg_pace) + (2.0 - (avg_pace - fastest_lap)) - (consistency * 50)
    podium_finish = (score > np.percentile(score, 70)).astype(int)
    
    return pd.DataFrame({'AvgPace': avg_pace, 'FastestLap': fastest_lap, 'PaceConsistency': consistency}), podium_finish

print("🏎️ Generating synthetic telemetry data...")
X, y = generate_synthetic_f1_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- MLFLOW EXPERIMENT TRACKING ---
mlflow.set_experiment("LightGBM_Podium_Classifier")

with mlflow.start_run():
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'learning_rate': 0.05,
        'max_depth': 6,
        'num_leaves': 31,
        'seed': 42
    }
    
    # Log parameters to MLflow
    mlflow.log_params(params)
    
    train_data = lgb.Dataset(X_train, label=y_train)
    model = lgb.train(params, train_data, num_boost_round=100)
    
    # Evaluate
    preds_proba = model.predict(X_test)
    preds_class = (preds_proba > 0.5).astype(int)
    
    acc = accuracy_score(y_test, preds_class)
    loss = log_loss(y_test, preds_proba)
    
    # Log metrics to MLflow
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("log_loss", loss)
    
    # Log the actual model
    mlflow.lightgbm.log_model(model, "model")
    
    print(f"✅ Training Complete. Accuracy: {acc:.4f} | Log Loss: {loss:.4f}")
    print("📊 Experiment logged to MLflow.")