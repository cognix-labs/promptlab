# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and wheel file
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for database
RUN mkdir -p /app/data

# Copy the database file if it exists (optional)
# COPY promptlab.db /app/data/promptlab.db

# Expose ports 8000 and 8001 for external access
EXPOSE 8000 8001

# Set the default command to run promptlab studio
CMD ["promptlab", "studio", "start", "-d", "/app/data/promptlab.db", "-p", "8000"]
