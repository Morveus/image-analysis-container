# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ollama-image-analysis.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "ollama-image-analysis.py"] 