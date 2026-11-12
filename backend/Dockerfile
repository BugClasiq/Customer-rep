FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Migrations run only when a database is configured; otherwise boot anyway
# so /api/health answers even with no DB provisioned (gunicorn binds $PORT;
# Railway/Render inject it, default 5000).
CMD ["sh", "-c", "if [ -n \"$DATABASE_URL\" ] || [ -n \"$DB_HOST\" ]; then flask db upgrade; else echo 'No database configured - skipping migrations'; fi && gunicorn -b 0.0.0.0:${PORT:-5000} run:app"]
