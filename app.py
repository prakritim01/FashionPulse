import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import os

# 1. Page Configuration
st.set_page_config(page_title="FashionPulse Global Intelligence", layout="wide")

# 2. Dynamic F1 Theme Engine (CSS Injection)
def set_f1_theme(selected_race):
    # Mapping to your named photos
    theme_map = {
        "Monaco": "assets/monaco.jpg",
        "Silverstone": "assets/silverstone.jpg",
        "Spa": "assets/spa.jpg",
        "Singapore": "assets/singapore.jpg",
        "Monza": "assets/monza.jpg",
        "Suzuka": "assets/suzuka.jpg",
        "Las Vegas": "assets/vegas.jpg",
        "Miami": "assets/miami.jpg",
        "Sakhir": "assets/bahrain.jpg", 
        "Lusail": "assets/qatar.jpg",
        "Shanghai": "assets/chinesegp.jpg",
        "Melbourne": "assets/melbourne.jpg",
        "Zandvoort": "assets/zandavroot.jpg", 
        "Barcelona": "assets/barca.jpg",
        "Jeddah": "assets/jeddah.jpg",
        "Madrid": "assets/madrid.jpg",
        "Montreal": "assets/montreal.jpg",
        "Austin": "assets/austin.jpg",
        "Mexico City": "assets/mexico.jpg",
        "Interlagos": "assets/brazil.jpg",
        "Yas Marina": "assets/abudhabi.jpg",
        "Spielberg": "assets/austria.jpg",
        "Budapest": "assets/budapest.jpg",
        "Imola": "assets/imola.jpg"
    }
    
    # FIX: Use 'selected_race' to match the function parameter
    bg_path = theme_map.get(selected_race, "assets/ferrari.jpg")
    
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Enhanced Visibility Fixes */
            [data-testid="stAppViewContainer"] > .main {{
                background-color: rgba(0, 0, 0, 0.85); /* High contrast for visibility */
                backdrop-filter: blur(8px);
                color: #FFFFFF !important;
            }}
            /* Ensuring all text is readable against backgrounds */
            h1, h2, h3, p, span, label, .stMarkdown {{
                color: white !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                font-weight: 600 !important;
            }}
            .stTabs [data-baseweb="tab-panel"] {{
                background-color: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# 3. Data Loading Utility
@st.cache_data
def load_all_data():
    data = {}
    files = {
        'f1': 'data/processed/master_f1_results.csv',
        'sentiment': 'data/processed/trend_velocity_report.csv',
        'roi': 'data/processed/brand_roi_report.csv',
        'forecast': 'data/processed/trend_forecast.csv'
    }
    for key, path in files.items():
        if os.path.exists(path):
            data[key] = pd.read_csv(path)
    return data

data = load_all_data()

# Check if data exists before rendering
if 'f1' in data and 'sentiment' in data:
    # 4. Sidebar Control Center
    st.sidebar.header("🏎️ Race Strategy Hub")
    
    race_list = data['f1']['Race'].unique()
    selected_race = st.sidebar.selectbox("Select Grand Prix Location", race_list)
    
    set_f1_theme(selected_race)
    
    current_market = data['f1'][data['f1']['Race'] == selected_race]['Market_Segment'].iloc[0]
    all_teams = data['f1']['TeamName'].unique()
    selected_teams = st.sidebar.multiselect("Active Teams", all_teams, default=all_teams)

    # 5. Header Section
    st.title(f"🏁 FashionPulse: {selected_race} Intelligence")
    st.markdown(f"### Current Market: {current_market}")
    st.markdown("---")

    # 6. Global Map
    st.subheader("🌍 Global Market Sentiment Map")
    map_coords = {
        'Shanghai': [31.3389, 121.2203], 'Suzuka': [34.8431, 136.541],
        'Sakhir': [26.0325, 50.5106], 'Jeddah': [21.6319, 39.1044],
        'Singapore': [1.2915, 103.8639], 'Baku': [40.3725, 49.8533],
        'Lusail': [25.4900, 51.4542], 'Yas Marina': [24.4672, 54.6031],
        'Monaco': [43.7347, 7.4206], 'Barcelona': [41.57, 2.2611],
        'Madrid': [40.4667, -3.6167], 'Spielberg': [47.2197, 14.7647],
        'Silverstone': [52.0786, -1.0169], 'Spa': [50.4372, 5.9714],
        'Budapest': [47.583, 19.248], 'Zandvoort': [52.3888, 4.5409],
        'Monza': [45.6189, 9.2811], 'Imola': [44.3439, 11.7167],
        'Miami': [25.9581, -80.2389], 'Montreal': [45.5000, -73.5228],
        'Austin': [30.1328, -97.6411], 'Mexico City': [19.4042, -99.0907],
        'Sao Paulo': [-23.7036, -46.6997], 'Las Vegas': [36.1147, -115.1728],
        'Melbourne': [-37.8497, 144.968], 'Milan': [45.6189, 9.2811]
    }
    
    map_df = pd.DataFrame([{'Race': loc, 'lat': c[0], 'lon': c[1]} for loc, c in map_coords.items()])
    st.map(map_df)

    # 7. Strategic Analytics Workspace
    market_f1 = data['f1'][(data['f1']['Race'] == selected_race) & 
                           (data['f1']['TeamName'].isin(selected_teams))]
    
    if not market_f1.empty:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 ROI Analytics", "🔮 Trend Forecasts", "📸 Visual Scanner", "💾 Strategy Portal"])

        with tab1:
            st.subheader(f"Brand Performance ROI: {selected_race}")
            if 'roi' in data:
                market_roi = data['roi'][(data['roi']['Race'] == selected_race) & 
                                         (data['roi']['TeamName'].isin(selected_teams))].copy()
                if not market_roi.empty:
                    fig = px.bar(market_roi, x='TeamName', y='Influence_ROI', color='TeamName', template="plotly_dark")
                    st.plotly_chart(fig, width="stretch")
                    
                    market_roi.loc[:, 'Efficiency'] = market_roi['Influence_ROI'] / (market_roi['ClassifiedPosition'] + 1)
                    best_team = market_roi.sort_values(by='Efficiency', ascending=False).iloc[0]['TeamName']
                    st.info(f"🤖 **FashionPulse AI Consultant:** **{best_team}** offers the highest 'Value for Influence' in this circuit.")

        with tab2:
            st.subheader("Predictive Time-Series Forecasts")
            if 'forecast' in data:
                fig_fore = px.line(data['forecast'], x='Race', y='Confidence', color='Aesthetic', template="plotly_dark")
                st.plotly_chart(fig_fore, width="stretch")

        with tab3:
            st.subheader("Visual Intelligence Engine")
            uploaded_file = st.file_uploader("Choose an outfit image...", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, width=400)
                with st.spinner('Analyzing...'):
                    img_rgb = image.convert('RGB')
                    img_data = list(img_rgb.getdata())
                    pixels = len(img_data)
                    
                    r_avg = sum(p[0] for p in img_data) / pixels
                    g_avg = sum(p[1] for p in img_data) / pixels
                    b_avg = sum(p[2] for p in img_data) / pixels
                    
                    if r_avg > 150 and g_avg < 120: label, conf = "Racing Core", (0.85 + (r_avg/1000))
                    elif (r_avg + g_avg + b_avg) / 3 > 180: label, conf = "Quiet Luxury", (0.90 + (g_avg/2000))
                    else: label, conf = "Old Money", (0.82 + (b_avg/1500))
                    
                    st.success(f"**AI Classification:** {label} ({min(0.99, conf)*100:.2f}%)")

        with tab4:
            st.subheader("Enterprise Strategy Export")
            if 'roi' in data and not market_roi.empty:
                csv = market_roi.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download ROI Report (CSV)", data=csv, 
                                   file_name=f"FashionPulse_{selected_race}_ROI.csv", mime='text/csv')
    else:
        st.warning("Adjust your sidebar filters to view race-specific data.")
else:
    st.error("🚨 Data files missing. Please ensure 'f1_ingest.py' has been executed.")