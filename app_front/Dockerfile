# ==============================================
# Stage 1: Builder - Installation des dépendances
# ==============================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies (create virtual environment)
RUN uv sync --no-dev --frozen

# ==============================================
# Stage 2: Runtime - Image de production légère
# ==============================================
FROM python:3.11-slim AS runtime

# Create non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy uv from builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Set Python path to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
