import gymnasium as gym
from gymnasium import spaces
import numpy as np
import sys
import os

# Ensure Python can find our app modules when running from the terminal
sys.path.insert(0, os.path.abspath('.'))
from app.optimization.reward_function import calculate_race_reward

class F1StrategyEnv(gym.Env):
    def __init__(self):
        super(F1StrategyEnv, self).__init__()
        self.total_laps = 50
        
        # Action Space: 4 possible moves per lap
        # 0 = Stay Out, 1 = Pit for Softs, 2 = Pit for Mediums, 3 = Pit for Hards
        self.action_space = spaces.Discrete(4)
        
        # Observation Space: What the AI "sees" [Current Lap, Tire Age, Current Compound]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]), 
            high=np.array([self.total_laps, self.total_laps, 2]), 
            dtype=np.float32
        )
        self.reset()
        
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.current_lap = 0
        self.tire_age = 0
        self.compound = 1 # Start the race on Mediums (1)
        return np.array([self.current_lap, self.tire_age, self.compound], dtype=np.float32), {}
        
    def step(self, action):
        pitted = False
        
        if action > 0: # The agent chose to pit
            pitted = True
            self.compound = action - 1 # Map action (1,2,3) to compound (0,1,2)
            self.tire_age = 0 # Fresh tires!
            
        # Calculate the reward based on the action taken
        # Base lap time is arbitrarily 90 seconds
        reward = calculate_race_reward(
            base_lap_time=90.0, 
            tire_age=self.tire_age, 
            compound=self.compound, 
            pitted=pitted
        )
        
        # Advance the race
        self.current_lap += 1
        self.tire_age += 1
        
        done = self.current_lap >= self.total_laps
        truncated = False
        
        obs = np.array([self.current_lap, self.tire_age, self.compound], dtype=np.float32)
        return obs, reward, done, truncated, {}