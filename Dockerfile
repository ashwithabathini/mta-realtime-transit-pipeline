# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy our requirements file first (efficient for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy our script into the container
COPY ingest_mta.py .

# Run the script when the container starts
CMD ["python", "ingest_mta.py"]