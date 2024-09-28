# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install any necessary system dependencies (if needed)
# You can add other dependencies if required by your app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that the Streamlit app runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "Home.py", "--server.address=0.0.0.0"]
