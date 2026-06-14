from stable_baselines3 import PPO
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from app.optimization.race_environment import F1StrategyEnv

def train_strategy_agent():
    print("🤖 Initializing Reinforcement Learning Strategy Agent...")
    env = F1StrategyEnv()
    
    # Tuned PPO Architecture for faster convergence on finite horizons:
    # ent_coef=0.05 forces the agent to aggressively explore random actions (like pitting)
    # n_steps=2048 updates the policy after observing larger chunks of data
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=0, 
        learning_rate=0.0005,
        n_steps=2048,
        batch_size=64,
        ent_coef=0.05, 
        seed=42  # Corrected from random_state to seed
    )
    
    # We increase simulations from 20k to 80k steps to let the long-term penalties settle in
    print("🚀 Simulating 80,000 race scenarios to find the mathematical optimum...")
    model.learn(total_timesteps=80000)
    
    os.makedirs('models_registry', exist_ok=True)
    model.save('models_registry/strategy_agent')
    print("✅ RL Strategy Agent trained and saved to models_registry/strategy_agent.zip")
    
    # --- Test the learned strategy immediately ---
    print("\n🏁 Testing learned strategy for a 50-lap race:")
    obs, _ = env.reset()
    compounds = ["Soft", "Medium", "Hard"]
    
    total_stops = 0
    for lap in range(50):
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, done, truncated, info = env.step(action)
        
        if action > 0:
            print(f"  🏎️  Lap {lap+1}: Agent decides to PIT for {compounds[action-1]} tires!")
            total_stops += 1
            
    if total_stops == 0:
        print("  ⚠️ Agent attempted a 0-stop race (Tires must have been screaming!)")
    else:
        print(f"📊 Strategy complete with an optimal {total_stops}-stop race.")

if __name__ == "__main__":
    train_strategy_agent()