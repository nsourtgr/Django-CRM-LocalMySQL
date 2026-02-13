FROM python:3.11-slim

WORKDIR /app

# Install system packages for mysqlclient and cryptography
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        pkg-config \
        libssl-dev \
        libmariadb-dev \
        libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt /app/

# Upgrade pip and install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app

# Entrypoint (adjust if needed)
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
