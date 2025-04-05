# Use official Prometheus image as a base
FROM prom/prometheus:latest

# Copy your custom configuration into the image
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose Prometheus port
EXPOSE 9090

# Start Prometheus with the config file
CMD [ "--config.file=/etc/prometheus/prometheus.yml" ]
