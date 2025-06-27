# Multi-stage build for minimal image size
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers

# Set working directory
WORKDIR /build

# Copy requirements first for better caching
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Install Python dependencies
RUN pip install --no-cache-dir --user -e .

# Copy source code
COPY dashtrash/ dashtrash/
COPY dashboard.yml .

# Final stage - minimal runtime image
FROM python:3.11-alpine

# Create non-root user
RUN addgroup -g 1001 dashtrash && \
    adduser -D -u 1001 -G dashtrash dashtrash

# Install runtime dependencies
RUN apk add --no-cache \
    procps \
    util-linux

# Copy installed packages from builder
COPY --from=builder /root/.local /home/dashtrash/.local

# Set up environment
ENV PATH="/home/dashtrash/.local/bin:$PATH"
ENV PYTHONPATH="/home/dashtrash/.local/lib/python3.11/site-packages"

# Create config directory
RUN mkdir -p /home/dashtrash/.config/dashtrash && \
    chown -R dashtrash:dashtrash /home/dashtrash

# Copy default config
COPY --chown=dashtrash:dashtrash dashboard.yml /home/dashtrash/.config/dashtrash/

# Switch to non-root user
USER dashtrash
WORKDIR /home/dashtrash

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD dashtrash --version || exit 1

# Default command
CMD ["dashtrash"]

# Labels for better metadata
LABEL org.opencontainers.image.title="dashtrash"
LABEL org.opencontainers.image.description="Terminal-based dashboard for real-time monitoring"
LABEL org.opencontainers.image.source="https://github.com/turancannb02/dashtrash"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.licenses="MIT" 