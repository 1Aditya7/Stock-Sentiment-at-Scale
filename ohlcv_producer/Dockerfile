# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (to allow Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ohlcv_producer.py .

# Run the producer
CMD ["python", "ohlcv_producer.py"]
