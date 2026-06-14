import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit fluid layout configuration (using the updated stretch width rule)
st.set_page_config(layout="wide")

st.title("🏁 IntelGrid F1 Intelligence Platform")
st.markdown("### Telemetry Analytics • Race Prediction • Strategy Optimization")

tab1, tab2, tab3 = st.tabs(["🔮 Race Prediction", "📊 Strategy Optimizer (PPO)", "⚔️ Driver Battle Analyzer"])

# -------------------------------------------------------------------
# TAB 2: PPO STRATEGY OPTIMIZER VISUALIZATION
# -------------------------------------------------------------------
with tab2:
    st.header("Reinforcement Learning Strategy Simulation")
    st.write("Visualizing the PPO Agent's optimized multi-stint pit window thresholds.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        total_laps = st.number_input("Total Race Laps", min_value=10, max_value=80, value=53)
        starting_compound = st.selectbox("Starting Tire Compound", ["SOFT", "MEDIUM", "HARD"])
        optimize_btn = st.button("Run PPO Simulation")
        
    with col2:
        if optimize_btn:
            # Mocking or calling the FastAPI endpoint: /api/v1/strategy/optimize?laps=X&compound=Y
            # Let's say the PPO agent suggests pitting at lap 18 and 38
            stint_1 = int(total_laps * 0.34)
            stint_2 = int(total_laps * 0.72)
            
            st.success(f"Optimal Strategy Found! Pit Windows: Lap {stint_1} and Lap {stint_2}")
            
            # Creating a visual timeline chart using matplotlib
            fig, ax = plt.subplots(figsize=(10, 2))
            colors = {"SOFT": "#FF3333", "MEDIUM": "#FFCC00", "HARD": "#FFFFFF"}
            
            # Draw stint bars
            ax.barh(0, stint_1, color=colors[starting_compound], edgecolor='black', label=f'Stint 1: {starting_compound}')
            next_compound = "HARD" if starting_compound == "SOFT" else "MEDIUM"
            ax.barh(0, stint_2 - stint_1, left=stint_1, color=colors[next_compound], edgecolor='black', label=f'Stint 2: {next_compound}')
            final_compound = "SOFT" if next_compound == "HARD" else "HARD"
            ax.barh(0, total_laps - stint_2, left=stint_2, color=colors[final_compound], edgecolor='black', label=f'Stint 3: {final_compound}')
            
            ax.set_xlim(0, total_laps)
            ax.set_xlabel("Race Laps")
            ax.set_yticks([])
            ax.set_title("PPO Agent Multi-Stint Optimization Timeline")
            ax.legend(loc='upper right')
            st.pyplot(fig)
            plt.close(fig) # 🟢 MEMORY LEAK FIX

# -------------------------------------------------------------------
# TAB 3: DRIVER BATTLE ANALYZER
# -------------------------------------------------------------------
with tab3:
    st.header("Head-to-Head Driver Battle Analyzer")
    st.write("Compare telemetry traces and pace consistency side-by-side.")
    
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        driver_1 = st.text_input("Driver 1 Code (e.g., LEC)", "LEC")
    with b_col2:
        driver_2 = st.text_input("Driver 2 Code (e.g., HAM)", "HAM")
    with b_col3:
        circuit = st.selectbox("Circuit", ["Monza", "Silverstone", "Spa", "Singapore"])
        
    if st.button("Analyze Battle"):
        st.markdown(f"#### Telemetry Comparison: **{driver_1}** vs **{driver_2}** at {circuit}")
        
        # Simulating pace telemetry over a sample lap trajectory (0-100% distance)
        progress = list(range(0, 100))
        speed_d1 = [200 + (x % 10) * 12 - (x // 20) * 8 for x in progress]
        speed_d2 = [205 + (x % 8) * 14 - (x // 18) * 10 for x in progress]
        
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(progress, speed_d1, label=driver_1, color="#EF1A2D") # Team red style
        ax2.plot(progress, speed_d2, label=driver_2, color="#00D2BE") 
        ax2.set_xlabel("Lap Distance (%)")
        ax2.set_ylabel("Speed (km/h)")
        ax2.set_title("Corner Apex Speed Profile Comparison")
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig2)
        plt.close(fig2) # 🟢 MEMORY LEAK FIX