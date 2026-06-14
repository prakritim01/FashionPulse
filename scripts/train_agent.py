import mlflow
import numpy as np
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym
from gymnasium import spaces

class SimplePitStrategyEnv(gym.Env):
    """A modern Gymnasium environment for F1 pit stop strategy."""
    def __init__(self):
        super(SimplePitStrategyEnv, self).__init__()
        self.action_space = spaces.Discrete(4) # 0: Stay, 1: Soft, 2: Medium, 3: Hard
        self.observation_space = spaces.Box(low=0, high=100, shape=(3,), dtype=np.float32)
        self.lap = 0
        self.tire_age = 0
        self.compound = 1.0 
        self.max_laps = 50

    def step(self, action):
        self.lap += 1
        self.tire_age += 1
        
        reward = 1.0 - (self.tire_age * 0.05) # Penalty for old tires
        if action > 0: 
            self.tire_age = 0
            reward -= 5.0 # Penalty for time lost in pit lane
            
        terminated = self.lap >= self.max_laps
        truncated = False
        
        state = np.array([self.lap, self.tire_age, self.compound], dtype=np.float32)
        return state, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.lap = 0
        self.tire_age = 0
        self.compound = 1.0
        state = np.array([self.lap, self.tire_age, self.compound], dtype=np.float32)
        return state, {}

# --- MLFLOW EXPERIMENT TRACKING ---
mlflow.set_experiment("PPO_Strategy_Optimizer")

print("🤖 Initializing Modern RL Agent Training...")
env = DummyVecEnv([lambda: SimplePitStrategyEnv()])

with mlflow.start_run():
    # Log RL Hyperparameters
    rl_params = {"learning_rate": 3e-4, "n_steps": 1024, "batch_size": 64, "total_timesteps": 5000}
    mlflow.log_params(rl_params)
    
    model = PPO("MlpPolicy", env, verbose=0, **{k:v for k,v in rl_params.items() if k != 'total_timesteps'})
    model.learn(total_timesteps=rl_params['total_timesteps'])
    
    # Save model locally and log artifact
    os.makedirs('models_registry', exist_ok=True)
    model.save("models_registry/strategy_agent.zip")
    mlflow.log_artifact("models_registry/strategy_agent.zip")
    
    print("✅ RL Agent Training Complete.")
    print("📊 Trajectories and rewards logged to MLflow.")