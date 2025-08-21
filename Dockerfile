# Use official slim Python image to reduce vulnerabilities
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Set environment variable to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Set environment variable to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Run FastAPI and Streamlit in the same container
CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
             streamlit run app/streamlit_app.py --server.port 8501 --server.enableCORS false"
