import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

def generate_phase3_dashboard():
    try:
        # 1. Load the Phase 2 data as the foundation
        f1_master = pd.read_csv('data/processed/master_f1_results.csv')
        velocity_df = pd.read_csv('data/processed/trend_velocity_report.csv')
        
        os.makedirs('docs', exist_ok=True)

        # 2. Create Subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Team Performance Consistency", "Aesthetic Velocity (Season Trend)"),
            specs=[[{"type": "xy"}, {"type": "xy"}]]
        )

        # 3. Add Team Bar Chart
        team_counts = f1_master['TeamName'].value_counts().reset_index()
        fig.add_trace(
            go.Bar(
                x=team_counts['TeamName'], 
                y=team_counts['count'], 
                name="Total Top 10s",
                marker_color='midnightblue'
            ),
            row=1, col=1
        )

        # 4. Add Aesthetic Trend Lines
        for aesthetic in velocity_df['Aesthetic'].unique():
            df_subset = velocity_df[velocity_df['Aesthetic'] == aesthetic]
            fig.add_trace(
                go.Scatter(
                    x=df_subset['Race'], 
                    y=df_subset['Confidence'],
                    mode='lines+markers',
                    name=aesthetic,
                    line=dict(width=4),
                    marker=dict(size=10)
                ),
                row=1, col=2
            )

        # --- PHASE 3: ADD INTERACTIVE UI BUTTONS ---
        # We create a toggle to switch between seeing "All Teams" or specific aesthetics
        fig.update_layout(
            updatemenus=[
                dict(
                    type="dropdown",
                    direction="down",
                    x=0.1,
                    y=1.2,
                    showactive=True,
                    buttons=list([
                        dict(
                            label="View All Aesthetics",
                            method="update",
                            args=[{"visible": [True] * (len(velocity_df['Aesthetic'].unique()) + 1)}]
                        ),
                        dict(
                            label="Focus: Quiet Luxury",
                            method="update",
                            args=[{"visible": [True] + [aesthetic == 'Quiet Luxury' for aesthetic in velocity_df['Aesthetic'].unique()]}]
                        )
                    ]),
                )
            ],
            title_text="🏎️ FashionPulse Phase 3: Interactive Sentiment Analytics",
            template="plotly_white",
            height=650
        )

        fig.write_html("docs/index.html")
        print("🎨 Phase 3 Interactive Dashboard successfully generated at docs/index.html")

    except Exception as e:
        print(f"❌ Dashboard Error: {e}")

if __name__ == "__main__":
    generate_phase3_dashboard()