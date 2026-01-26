import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

def generate_phase2_dashboard():
    try:
        # 1. Load the new Phase 2 data
        f1_master = pd.read_csv('data/processed/master_f1_results.csv')
        velocity_df = pd.read_csv('data/processed/trend_velocity_report.csv')
        
        os.makedirs('docs', exist_ok=True)

        # 2. Create Subplots: (1 row, 2 columns)
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("F1 Season Performance (Top Teams)", "Aesthetic Velocity (The Fashion Pulse)"),
            specs=[[{"type": "xy"}, {"type": "xy"}]]
        )

        # 3. Add F1 Master Bar Chart
        # Showing which teams appeared in the Top 10 most often across the season
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

        # 4. Add the Multi-Line Trend Chart (The Phase 2 Highlight)
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

        fig.update_layout(
            title_text="🏎️ FashionPulse Phase 2: Season Momentum & Trend Velocity",
            template="plotly_white",
            height=600
        )

        fig.write_html("docs/index.html")
        print("🎨 Phase 2 Dashboard generated at docs/index.html")

    except Exception as e:
        print(f"❌ Dashboard Error: {e}")

if __name__ == "__main__":
    generate_phase2_dashboard()