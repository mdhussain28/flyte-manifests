FROM python:3.9-slim

WORKDIR /app

# Install uv
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy project config & src package
COPY pyproject.toml .
ENV UV_HTTP_TIMEOUT=120
RUN uv sync
COPY src/ ./src/

# Make src a proper Python package
RUN touch src/__init__.py

# Install package in editable mode
RUN uv pip install --no-cache-dir -e .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV MLFLOW_TRACKING_URI=http://192.168.100.11:30050

# Default command
CMD ["pyflyte", "run", "src/workflows/linear-regression.py", "ml_workflow", "--n_samples", "1000", "--n_features", "12"]
