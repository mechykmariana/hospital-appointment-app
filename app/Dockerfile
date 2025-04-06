# Use Python official image
FROM python:3.8-slim

WORKDIR /app

# Install Node.js for the frontend
RUN apt-get update && \
    apt-get install -y nodejs npm

# Copy requirements.txt and install dependencies
COPY requirements.txt .

# Install library
RUN pip install psycopg2-binary

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ /app/frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

WORKDIR /app
# Copy the backend and frontend code
COPY backend/ /app/backend/

# Move React build to Flask static directory
RUN mkdir -p /app/backend/static && cp -r /app/frontend/build/* /app/backend/static/

# Expose ports
#EXPOSE 3000
EXPOSE 4000

WORKDIR /app/backend
# Run the application
CMD ["sh", "-c", "cd /app/backend && python app.py"]
