import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import os
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="FashionPulse Global Intelligence", layout="wide")

# 2. GLOBAL PREMIUM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

html, body, .stMarkdown, p, h1, h2, h3, span, label, li {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Dynamic F1 Theme Engine
def set_f1_theme(selected_race=None):
    bg_path = "assets/ferrari.jpg"
    if selected_race:
        race_lower = selected_race.lower()
        if "monaco" in race_lower: bg_path = "assets/monaco.jpg"
        elif "silverstone" in race_lower: bg_path = "assets/silverstone.jpg"
        elif "spa" in race_lower: bg_path = "assets/spa.jpg"
        elif "singapore" in race_lower: bg_path = "assets/singapore.jpg"
        elif "monza" in race_lower: bg_path = "assets/monza.jpg"

    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(10, 15, 30, 0.35), rgba(10, 15, 30, 0.65)), url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .stTabs [data-baseweb="tab-panel"] {{
                background-color: rgba(0, 0, 0, 0.45);
                padding: 25px;
                border-radius: 16px;
            }}
            </style>
            """, unsafe_allow_html=True
        )

# 4. Data Loading Utility
def load_all_data(year):
    data = {}
    f1_path = f'data/processed/f1_results_{year}.csv'
    if os.path.exists(f1_path):
        try:
            data['f1'] = pd.read_csv(f1_path)
        except Exception as e:
            st.error(f"Could not read F1 CSV: {e}")
    
    files = {
        'sentiment': 'data/processed/trend_velocity_report.csv',
        'roi': 'data/processed/brand_roi_report.csv',
        'forecast': 'data/processed/trend_forecast.csv'
    }
    for key, path in files.items():
        if os.path.exists(path):
            try:
                data[key] = pd.read_csv(path)
            except:
                pass
    return data

# 5. Top-Level Control Center
st.markdown("### Enterprise Strategy Controls")
col_c1, col_c2 = st.columns([1, 2])

with col_c1:
    selected_year = st.selectbox("Select Season", [2024, 2025, 2026], index=1)

# API Key Resolution
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY"):
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass

# --- THE BULLETPROOF ERROR SHIELD ---
try:
    data = load_all_data(selected_year)

    if 'f1' not in data:
        set_f1_theme()
        st.warning(f"No F1 database file found for {selected_year}. Please put 'f1_results_{selected_year}.csv' in your data/processed/ folder.")
    elif data['f1'].empty:
        set_f1_theme()
        st.warning(f"The CSV file for {selected_year} was found, but it is completely empty inside!")
    elif 'EventName' not in data['f1'].columns:
        set_f1_theme()
        st.error(f"CRITICAL CSV ERROR: Your file is missing the 'EventName' column. The columns inside your file are: {list(data['f1'].columns)}")
    else:
        race_list = [str(r) for r in data['f1']['EventName'].dropna().unique() if str(r).strip() != ""]
        
        if len(race_list) > 0:
            with col_c2:
                selected_race = st.selectbox("Grand Prix Location", race_list)
                
            set_f1_theme(selected_race)
            st.markdown("---")
            st.title(f"FashionPulse: {selected_race} ({selected_year}) Intelligence")
            st.markdown("---")

            main_col, side_col = st.columns([2.5, 1])
            
            with main_col:
                tab_cal, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Season Calendar", "🏁 Race Results", "📊 ROI Analytics", "📈 Trend Forecasts", "✨ Vision Engine", "💾 Export Data"])

                with tab_cal:
                    st.subheader(f"FIA Formula 1 World Championship - {selected_year}")
                    st.write("Current season progression based on database logs.")
                    
                    statuses = []
                    try:
                        current_idx = race_list.index(selected_race)
                    except ValueError:
                        current_idx = -1

                    for idx, r in enumerate(race_list):
                        if idx < current_idx:
                            statuses.append("🟢 Completed")
                        elif idx == current_idx:
                            statuses.append("📍 Current Selection")
                        else:
                            statuses.append("⏳ Upcoming")
                    
                    schedule_df = pd.DataFrame({
                        "Round": range(1, len(race_list) + 1),
                        "Grand Prix": race_list,
                        "Status": statuses
                    })
                    
                    st.dataframe(schedule_df, width='stretch', hide_index=True)

                with tab1:
                    st.subheader(f"Official Race Classification: {selected_race}")
                    race_data = data['f1'][data['f1']['EventName'] == selected_race]
                    display_cols = [col for col in ['Position', 'FullName', 'TeamName', 'Points', 'Status'] if col in race_data.columns]
                    if display_cols:
                        st.table(race_data[display_cols])
                    else:
                        st.dataframe(race_data)

                with tab2:
                    st.subheader("Brand Performance ROI")
                    if 'roi' in data:
                        market_roi = data['roi'][data['roi']['Race'] == selected_race].copy()
                        if not market_roi.empty:
                            fig = px.bar(market_roi, x='TeamName', y='Influence_ROI', color='TeamName', template="plotly_dark")
                            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig, width='stretch')
                        else:
                            st.info("Legacy ROI data not mapped for this newly fetched race yet.")

                with tab3:
                    st.subheader("Predictive Time-Series Forecasts")
                    if 'forecast' in data:
                        fig_fore = px.line(data['forecast'], x='Race', y='Confidence', color='Aesthetic', template="plotly_dark")
                        fig_fore.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig_fore, width='stretch')

                with tab4:
                    st.subheader("AI Visual Intelligence Engine")
                    st.write("Upload paddock or streetwear imagery to analyze alignment with high-fashion archetypes.")
                    uploaded_file = st.file_uploader("Choose an outfit image...", type=["jpg", "jpeg", "png"])
                    if uploaded_file:
                        image = Image.open(uploaded_file)
                        st.image(image, width='stretch', caption="Paddock Specimen Acquired")
                        if st.button("Run AI Vision Scan", type="primary"):
                            if not api_key: 
                                st.error("Vision System Configuration Missing. Please add your key to a .env file.")
                            else:
                                with st.spinner("Analyzing textiles and aesthetic signatures..."):
                                    try:
                                        # Migrated to the new google.genai package
                                        client = genai.Client(api_key=api_key)
                                        prompt = "You are a high-fashion AI strategist for a luxury brand sponsoring a Formula 1 team. Classify this outfit heavily into one of three aesthetic categories: 1. 'Old Money' 2. 'Quiet Luxury' 3. 'Racing Core'. Give a short 2-sentence breakdown."
                                        
                                        response = client.models.generate_content(
                                            model='gemini-2.5-flash',
                                            contents=[prompt, image]
                                        )
                                        
                                        st.success("Analysis Complete")
                                        st.markdown(response.text)
                                    except Exception as e:
                                        st.error(f"Vision Engine offline: {e}")

                with tab5:
                    st.subheader("Enterprise Strategy Export")
                    csv = race_data.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Race Report (CSV)", data=csv, file_name=f"FashionPulse_{selected_race}_Report.csv", mime='text/csv')

            with side_col:
                with st.container(border=True):
                    st.subheader("Paddock Trivia")
                    st.write("Test your F1 knowledge.")
                    
                    trivia_questions = [
                        {"q": "What is the minimum weight of an F1 car?", "opts": ["750 kg", "798 kg", "850 kg"], "ans": "798 kg"},
                        {"q": "What does 'DRS' stand for?", "opts": ["Drag Reduction System", "Downforce Rear Spoiler"], "ans": "Drag Reduction System"}
                    ]
                    
                    if 'q_idx' not in st.session_state:
                        st.session_state.q_idx = 0
                        st.session_state.score = 0
                        st.session_state.answered = False
                        
                    if st.session_state.q_idx < len(trivia_questions):
                        q = trivia_questions[st.session_state.q_idx]
                        st.markdown(f"**Q:** {q['q']}")
                        
                        if not st.session_state.answered:
                            choice = st.radio("Select an option:", q['opts'], key=f"radio_{st.session_state.q_idx}")
                            if st.button("Submit Answer", width='stretch'):
                                st.session_state.last_result = (choice == q['ans'])
                                if st.session_state.last_result: 
                                    st.session_state.score += 1
                                else: 
                                    st.session_state.correct_ans = q['ans']
                                st.session_state.answered = True
                                st.rerun()
                        else:
                            if st.session_state.last_result: 
                                st.success("🏁 Correct!")
                                st.balloons()
                            else: 
                                st.error(f"⚠️ Incorrect. Answer: {st.session_state.correct_ans}")
                                
                            if st.button("Next Question", width='stretch'):
                                st.session_state.q_idx += 1
                                st.session_state.answered = False
                                st.rerun()
                    else:
                        st.info(f"Final Score: {st.session_state.score} / {len(trivia_questions)}")
                        if st.button("Restart Module", width='stretch'):
                            st.session_state.q_idx = 0
                            st.session_state.score = 0
                            st.session_state.answered = False
                            st.rerun()
        else:
            set_f1_theme()
            st.warning("No race events found in the database yet.")

except Exception as e:
    st.error(f"🚨 FATAL APP ERROR CAUGHT: {str(e)}")