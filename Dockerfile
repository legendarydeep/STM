# ==============================================================================
# Dockerfile: Student Task Management System
# Lightweight, secure, containerized Python/Flask environment
# ==============================================================================

# 1. Official lightweight Python base image
FROM python:3.11-slim

# 2. Environment flags for Python inside containers:
#    - PYTHONDONTWRITEBYTECODE: prevents Python from writing .pyc files
#    - PYTHONUNBUFFERED: allows real-time stdout/stderr log output
#    - PORT: default listening port
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_APP=app.py

# 3. Set working directory inside container
WORKDIR /app

# 4. Create non-root system user for improved container security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/instance && \
    chown -R appuser:appuser /app

# 5. Copy and install Python dependencies first (leverages Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application source code
COPY --chown=appuser:appuser . .

# 7. Declare persistence volume for SQLite database directory
#    Ensures database files inside /app/instance persist even if container is destroyed
VOLUME ["/app/instance"]

# 8. Switch to non-root user
USER appuser

# 9. Expose application port
EXPOSE 5000

# 10. Run Flask application listening on all interfaces (0.0.0.0)
CMD ["python", "app.py"]
