def calculate_race_reward(base_lap_time, tire_age, compound, pitted):
    """
    Calculates the reward based ONLY on time lost (Delta).
    Removes the constant base_lap_time so the neural network can see the variance clearly.
    """
    
    # 1. Base Pace Offsets (Softs are faster, Hards are slower)
    base_pace_modifiers = {
        0: -1.0,  # Softs gain 1 second
        1: 0.0,   # Mediums are baseline
        2: 1.0    # Hards lose 1 second
    }
    
    # 2. Normal Degradation (Seconds lost per lap)
    linear_deg_rates = {
        0: 0.10,  
        1: 0.06,  
        2: 0.03   
    }
    
    # 3. The "Cliff"
    tire_cliffs = {
        0: 15,  
        1: 25,  
        2: 38   
    }
    
    # Calculate the time lost due to compound and age
    pace_modifier = base_pace_modifiers.get(compound, 0.0)
    deg_penalty = tire_age * linear_deg_rates.get(compound, 0.05)
    total_lap_penalty = pace_modifier + deg_penalty
    
    # 4. Enforce the Cliff 
    cliff = tire_cliffs.get(compound, 20)
    if tire_age > cliff:
        # Quadratically scale time loss past the cliff limit
        total_lap_penalty += 0.5 * ((tire_age - cliff) ** 2)
        
    # Standard F1 pit lane time loss
    pit_loss = 22.0 if pitted else 0.0
    
    # THE FIX: Reward is ONLY the negative time lost, ignoring the 90s base lap time.
    reward = -(total_lap_penalty + pit_loss)
    
    return reward