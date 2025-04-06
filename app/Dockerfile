# Use Python official image
FROM python:3.8-slim-buster

# Install Node.js for the frontend
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    apt-get clean

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install library
RUN pip install psycopg2-binary

RUN pip install --no-cache-dir -r requirements.txt

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Serve frontend from backend
WORKDIR /app

EXPOSE 4000

# Serve static files from Flask or with nginx (option below)

CMD ["sh", "-c", "cd /app/backend && python app.py"]
