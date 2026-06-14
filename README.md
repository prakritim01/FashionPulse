#  IntelGrid F1

### AI-Powered Formula 1 Intelligence Platform

IntelGrid F1 is a full-stack Formula 1 intelligence platform that combines machine learning, telemetry analytics, reinforcement learning, predictive modeling, sentiment intelligence, and race strategy optimization into a unified dashboard.

Built using FastAPI, Streamlit, LightGBM, PPO Reinforcement Learning, MLflow, Docker, and Plotly, the platform transforms raw motorsport data into actionable race intelligence.

## 🌐 Live Demo
 Live Application:
https://intelgrid-f1.onrender.com

 GitHub Repository:
https://github.com/prakritim01/IntelGrid-F1

##  Project Overview
Formula 1 generates massive volumes of data from races, telemetry streams, weather conditions, tire performance, driver behavior, and team strategies.
IntelGrid F1 leverages Data Engineering, Machine Learning, Reinforcement Learning, and MLOps practices to convert this data into meaningful insights and strategic recommendations.

The platform enables users to:
- Analyze race and driver performance
- Explore real telemetry data
- Predict race outcomes
- Simulate pit-stop strategies
- Monitor fan sentiment
- Visualize performance trends
- Compare drivers across multiple metrics

#  Core Features

##  Race Center
- Formula 1 race calendar
- Circuit information
- Session tracking
- Event overview dashboard

##  Prediction Hub
Machine Learning powered race predictions:
- Podium Probability Prediction
- Top-10 Finish Prediction
- Performance Forecasting
- Driver Ranking Analysis

### Models
- LightGBM
- Random Forest
- Ensemble Learning

##  Real Telemetry Explorer
Interactive telemetry analytics powered by FastF1.

### Metrics
- Speed
- Throttle
- Brake
- RPM
- Gear
- DRS Usage

### Capabilities
- Driver selection
- Race selection
- Lap-level analysis
- Interactive Plotly visualizations

##  Driver Battle Analyzer
Head-to-head driver comparison system.

### Compare
- Average Pace
- Sector Performance
- Consistency
- Race Performance
- Telemetry Metrics

##  Strategy Optimizer
AI-assisted race strategy recommendations.

### Inputs
- Driver
- Track
- Weather
- Starting Position
- Tire Compound

### Outputs
- Optimal Pit Windows
- Tire Strategy Recommendations
- Expected Finishing Position

## 🤖 PPO Strategy Simulator
Reinforcement Learning powered race simulation engine.

### Features
- Race Environment Modeling
- Reward Optimization
- Pit Stop Decision Making
- Strategy Evaluation

Framework:
- Stable Baselines3 PPO

##  Sentiment Intelligence
Natural Language Processing based sentiment analysis.
Tracks:
- Driver Sentiment
- Team Sentiment
- Fan Reactions
- Trend Momentum

## Visual Intelligence Engine
Computer Vision powered analysis system.

### Capabilities
- Visual Classification
- Brand Visibility Analysis
- Visual Trend Detection

##  MLOps & Experiment Tracking
Integrated MLflow workflow.

### Tracks
- Experiments
- Model Versions
- Metrics
- Training Runs
- Artifacts

#  System Architecture

```text
FastF1 API
      │
      ▼
Data Ingestion Layer
      │
      ▼
Feature Engineering
      │
      ▼
Machine Learning Models
      │
      ▼
PPO Strategy Engine
      │
      ▼
FastAPI Backend
      │
      ▼
Streamlit Dashboard
      │
      ▼
End User
```

#  Technology Stack

## Frontend
- Streamlit
- Plotly

## Backend
- FastAPI
- Python

## Machine Learning
- LightGBM
- Scikit-Learn
- Pandas
- NumPy

## Reinforcement Learning
- Stable Baselines3
- PPO

## Data Engineering
- FastF1
- FIA Data Sources

## MLOps
- MLflow

## DevOps
- Docker
- GitHub Actions
- Render

#  Project Structure

```text
IntelGrid-F1/

├── .github/
│   └── workflows/
│
├── app/
│   ├── dashboard/
│   ├── ingestion/
│   ├── models/
│   ├── optimization/
│   ├── services/
│   └── utils/
│
├── assets/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── mlruns/
│
├── models_registry/
│
├── tests/
│
├── deployment/
│
├── requirements.txt
├── README.md
└── LICENSE
```

#  Installation

Clone the repository:

```bash
git clone https://github.com/prakritim01/IntelGrid-F1.git
```

Move into project:

```bash
cd IntelGrid-F1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI backend:

```bash
uvicorn app.api.main:app --reload
```

Run Streamlit dashboard:

```bash
streamlit run app/dashboard/streamlit_app.py
```

#  Example Use Cases

### Race Prediction
Predict:
- Podium Finishes
- Top-10 Finishes
- Expected Driver Performance

### Telemetry Analysis
Analyze:
- Speed Traces
- Brake Usage
- Throttle Application
- DRS Deployment

### Strategy Optimization
Simulate:
- Pit Stop Timing
- Tire Strategies
- Race Outcomes

### Driver Comparison
Compare:
- Pace
- Consistency
- Telemetry
- Historical Performance

# Future Enhancements

- Tire Degradation Forecasting
- Dynamic Weather Impact Modeling
- Multi-Race Simulations
- Cloud-Native Deployment
- Advanced RL Strategy Training
- Distributed Experiment Tracking
- Multi-Season Analytics

# 📌 Why IntelGrid F1?

Unlike traditional Formula 1 dashboards, IntelGrid F1 combines:

✅ Data Engineering

✅ Machine Learning

✅ Reinforcement Learning

✅ Telemetry Analytics

✅ Strategy Optimization

✅ MLOps

✅ Interactive Visualization

into a single AI-powered motorsport intelligence platform.


#  Support

If you found this project interesting:

Star the repository

🍴 Fork the repository

🚀 Contribute enhancements

🏎️ Explore Formula 1 through AI
