# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for ML libraries 
# (Added libgomp1 specifically to prevent LightGBM crashes on slim images)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose the ports for Streamlit and FastAPI
EXPOSE 8501 8000

# Make the dual-boot script executable
RUN chmod +x start.sh

# Start the application using your routing script
CMD ["bash", "start.sh"]