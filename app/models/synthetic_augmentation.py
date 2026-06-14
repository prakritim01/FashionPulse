import pandas as pd
import numpy as np
import lightgbm as lgb
import joblib
import os

def upgrade_podium_model():
    print("🧠 Augmenting Podium Model with Generalized Synthetic Season Data...")
    np.random.seed(42)

    # 1. Generate 10,000 synthetic race stints across all track lengths (70s to 120s laps)
    n_samples = 10000
    avg_paces = np.random.uniform(70.0, 120.0, n_samples)
    
    # Fastest lap is naturally a bit quicker than the average pace
    fastest_laps = avg_paces - np.random.uniform(0.5, 2.5, n_samples)
    
    # Consistency variance (lower is better)
    variances = np.random.uniform(0.01, 1.5, n_samples)

    df = pd.DataFrame({
        'AvgPace': avg_paces,
        'FastestLap': fastest_laps,
        'PaceConsistency': variances
    })

    # 2. Define the exact mathematical rule for a podium finish
    # To get a podium, your variance must be very low, and your pace must be elite.
    # We create a "Performance Score" (Lower is better)
    performance_score = df['AvgPace'] + (df['PaceConsistency'] * 15)
    
    # The top 15% of performance scores in this dataset represent podium finishes
    threshold = performance_score.quantile(0.15) 
    df['Podium'] = (performance_score <= threshold).astype(int)

    # 3. Train the upgraded LightGBM Classifier
    print("🚀 Training Upgraded LightGBM Classifier...")
    X = df[['AvgPace', 'FastestLap', 'PaceConsistency']]
    y = df['Podium']

    model = lgb.LGBMClassifier(
        n_estimators=300, 
        learning_rate=0.05, 
        random_state=42, 
        verbose=-1
    )
    model.fit(X, y)

    # 4. Save to Registry
    os.makedirs('models_registry', exist_ok=True)
    joblib.dump(model, 'models_registry/podium_model.pkl')
    print("✅ Generalized Model Saved! Your dashboard will now react dynamically to any lap time.")

if __name__ == "__main__":
    upgrade_podium_model()