FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app/api
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir -r /app/api/requirements.txt
COPY api/app /app/api/app
COPY database /app/database
COPY ["SPOT_KnightHacks_Challenge_Kit Part One/02_DATA", "/app/SPOT_KnightHacks_Challenge_Kit Part One/02_DATA"]
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
