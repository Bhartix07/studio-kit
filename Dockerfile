# Dockerfile for STUDIO OS Visual Kit
# Uses Playwright official image which has Chromium + all deps pre-installed

FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# Install ffmpeg for MP4 rendering
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Ensure out/ and build/ directories exist
RUN mkdir -p out build

# Render sets PORT env var; default 5000 for local
ENV PORT=5000

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
