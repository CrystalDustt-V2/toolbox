# Production-grade ToolBox CLI Dockerfile
FROM python:3.11-slim

# Install system dependencies (Engines)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tesseract-ocr \
    libreoffice \
    poppler-utils \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install ToolBox and its dependencies
RUN pip install --no-cache-dir -e .

# Create a volume for data processing
VOLUME /data
WORKDIR /data

# Default command
ENTRYPOINT ["toolbox"]
CMD ["--help"]
