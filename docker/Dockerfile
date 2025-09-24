# Stage 1: builder
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies (only in builder)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a temp dir
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: runtime
FROM python:3.13-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy only your application code
COPY . .

# Environment variables
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose gradio port
EXPOSE 7860

# Run the app
CMD ["python", "app/gradio_app.py"]
