# Use Python 3.8 base image
FROM python:3.8-slim

# Install dependencies for Python and Node.js
RUN apt-get update && \
    apt-get install -y nodejs npm curl && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy and install backend Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL driver separately
RUN pip install psycopg2-binary

# Copy backend and frontend source
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Install frontend dependencies
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install

# Build frontend (optional if you're using static files)
# RUN npm run build

# Go back to root app folder
WORKDIR /app

# Expose ports (optional unless needed)
EXPOSE 4000
EXPOSE 3000

# Start both backend and frontend
CMD ["sh", "-c", "cd /app/backend && python app.py & cd /app/frontend && npm start"]
