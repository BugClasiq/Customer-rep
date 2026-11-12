# Root image: builds the whole app as one service.
# Flask serves the static frontend, /api/* (auth, chat, health) and needs no nginx.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . .

WORKDIR /app/backend

EXPOSE 5000

# Migrations are idempotent; gunicorn binds to $PORT (Railway/Render inject it, default 5000).
CMD ["sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:${PORT:-5000} run:app"]
