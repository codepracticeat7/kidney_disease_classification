# Start from Python
FROM python:3.8-slim-bullseye

# Proxy args (if needed)
ARG http_proxy
ARG https_proxy
ENV http_proxy=$http_proxy
ENV https_proxy=$https_proxy

# Install system dependencies + Azure CLI
RUN echo "Acquire::http::Proxy \"$http_proxy\";" >> /etc/apt/apt.conf.d/01proxy && \
    echo "Acquire::https::Proxy \"$https_proxy\";" >> /etc/apt/apt.conf.d/01proxy && \
    apt-get update -y && \
    apt-get install -y curl gnupg build-essential && \
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    rm -rf /var/lib/apt/lists/*


# Copy your app
WORKDIR /app
COPY . .
# Install Python dependencies for ML + Web app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# Expose port for web app
EXPOSE 8000

# Start app (FastAPI / Flask / Django etc.)
CMD ["python", "app.py"]

