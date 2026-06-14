from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import predictions

# Initialize the production API
app = FastAPI(
    title="IntelGrid F1 Intelligence API",
    description="Backend AI Engine for Formula 1 Race Analytics & Strategy",
    version="1.0.0"
)

# Enable CORS so the Streamlit frontend can securely communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the prediction routes
# (Heavy ML libraries are lazy-loaded inside these routes, keeping boot RAM near zero)
app.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])

# Standard health check endpoint for Render's load balancer
@app.get("/")
def health_check():
    return {
        "system": "IntelGrid F1", 
        "status": "Online", 
        "modules": ["Data Ingestion", "Machine Learning", "NLP"],
        "memory_optimization": "Active"
    }