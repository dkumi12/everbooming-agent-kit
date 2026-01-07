# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install system dependencies (optional but useful)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Make startup script executable
RUN chmod +x start.sh

# Expose Streamlit port (Railway will override this)
EXPOSE 8501

# Use startup script that handles dynamic PORT
CMD ["./start.sh"]
