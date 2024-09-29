# Use an official Python runtime as a parent image
FROM docker.io/python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install any necessary system dependencies (if needed)
# You can add other dependencies if required by your app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file (if you have one)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Apply cron job and Set the entry point command
CMD python3 src/main.py