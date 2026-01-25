import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

def generate_dashboard():
    # Load our latest processed data
    try:
        f1_df = pd.read_csv('data/processed/monaco_2025_results.csv').head(5)
        sent_df = pd.read_csv('data/processed/fashion_sentiment_sample.csv')
        
        # Ensure the docs folder exists for GitHub Pages
        os.makedirs('docs', exist_ok=True)

        # Create a subplot: 1 row, 2 columns
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("F1 Top 5 Finishers (Monaco)", "Fashion Aesthetic Distribution"),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )

        # 1. F1 Bar Chart (Rank vs Team)
        fig.add_trace(
            go.Bar(
                x=f1_df['Abbreviation'], 
                y=[5, 4, 3, 2, 1], 
                text=f1_df['TeamName'],
                name="Race Rank", 
                marker_color='midnightblue'
            ),
            row=1, col=1
        )

        # 2. Updated Aesthetic Pie Chart (Matches your new AI logic)
        aesthetic_counts = sent_df['Aesthetic'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=aesthetic_counts.index, 
                values=aesthetic_counts.values, 
                name="Aesthetics",
                marker=dict(colors=['#FF69B4', '#DAA520', '#000000']) # Fashion-themed colors
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text="🏎️ FashionPulse: Real-time F1 & Luxury Sentiment Insights",
            template="plotly_white",
            showlegend=True
        )

        # Save to the docs folder so it updates on your live website
        fig.write_html("docs/index.html")
        print("🎨 Dashboard successfully updated at docs/index.html")

    except FileNotFoundError:
        print("❌ Error: Processed data not found. Please run f1_ingest.py and sentiment_analyzer.py first!")

if __name__ == "__main__":
    generate_dashboard()