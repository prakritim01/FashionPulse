# 🏎️ FashionPulse: Interactive AI Analytics for F1 & Luxury Trends

![Update FashionPulse Data](https://github.com/prakritim01/FashionPulse/actions/workflows/update_pulse.yml/badge.svg)

## 📌 Project Vision
FashionPulse is a professional-grade AI pipeline that quantifies the relationship between high-performance sports and luxury consumer sentiment. By mapping F1 race results against social discourse, the platform provides a "Trend Velocity" score for luxury brands to measure sponsorship impact.

## 🚀 Phase 3: Interactive Features
* **Live Filtering:** Interactive Plotly dashboard allowing users to toggle between aesthetics like *Quiet Luxury*, *Old Money*, and *Racing Chic*.
* **Temporal Velocity Engine:** Time-series analysis tracking trend momentum across the 2025 season (Monaco, Miami, Las Vegas).
* **Autonomous DevOps:** Fully self-healing CI/CD pipeline using GitHub Actions to refresh analytics every Monday post-race.

## 🧠 Technical Architecture
* **NLP Engine:** `HuggingFace Transformers` (DistilBERT) for high-fidelity sentiment classification.
* **Data Engineering:** Automated ETL using `FastF1` for real-time race telemetry ingestion.
* **Visualization:** Custom `Plotly` multi-trace dashboards hosted via GitHub Pages.

## 📊 Live Dashboard
[Explore the Interactive Data Here](https://prakritim01.github.io/FashionPulse/)