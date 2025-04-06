# Use Python official image
FROM python:3.8-slim

# Install Node.js for the frontend
RUN apt-get update && \
    apt-get install -y nodejs npm

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install library
RUN pip install psycopg2-binary

RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies
COPY frontend/package*.json /app/frontend/
RUN cd /app/frontend && npm install

# Copy the backend and frontend code
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

# Expose the port that the app will run on
#EXPOSE 4000 3000

ENV PORT=3000

WORKDIR /app
# Run the application
CMD ["sh", "-c", "cd /app/backend && python app.py & cd /app/frontend && npm start"]
