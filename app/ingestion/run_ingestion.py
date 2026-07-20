# app/ingestion/run_ingestion.py
import sys
import os

# Ensure the app module can be found when running from the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import your new modular loaders
from app.ingestion import fastf1_loader
from app.ingestion import schedule_loader
from app.ingestion import standings_loader
from app.ingestion import weather_loader

def main():
    print("Starting F1 data ingestion...")
    # Add your execution logic here based on how your loaders are structured
    # fastf1_loader.load_data()
    # schedule_loader.update_schedule()
    print("Ingestion complete.")

if __name__ == "__main__":
    main()