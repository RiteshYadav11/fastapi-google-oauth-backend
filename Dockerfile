# --- Stage 1: Builder ---
FROM python:3.11.5-alpine3.18 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    make \
    bash \
    && pip install --upgrade pip wheel setuptools

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --- Stage 2: Final Image ---
FROM python:3.11.5-alpine3.18

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    PATH="/opt/venv/bin:$PATH" \
    TZ=UTC

WORKDIR /code

# Install runtime dependencies only
RUN apk add --no-cache \
    postgresql-libs \
    curl \
    bash \
    tzdata && \
    rm -rf /var/cache/apk/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY ./app ./app
COPY alembic.ini .
COPY migrations ./migrations
COPY .env .

# Create non-root user and change ownership
RUN addgroup -S app && adduser -S app -G app && \
    chown -R app:app /code /opt/venv

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]