#!/bin/bash

if [ "$SERVICE_TYPE" == "API" ]; then
    echo "Booting the FastAPI Backend..."
    uvicorn app.api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1

elif [ "$SERVICE_TYPE" == "DASHBOARD" ]; then
    echo "Booting the Streamlit Dashboard..."
    # Updated path to point to the correct 15-feature dashboard
    streamlit run app/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true

else
    echo "No SERVICE_TYPE defined! Falling back to dual-boot (warning: high RAM usage)..."
    uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --workers 1 --limit-concurrency 10 &
    # Updated path here as well for the dual-boot fallback
    streamlit run app/app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true
fi