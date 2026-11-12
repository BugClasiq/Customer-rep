# Root image: builds the app as one service.
# Entrypoint is the Gradio Support AI Assistant (python run.py).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP="app:create_app()" \
    GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . .

WORKDIR /app/backend

EXPOSE 7860

# Migrations run only when a database is configured; otherwise boot anyway.
CMD ["sh", "-c", "if [ -n \"$DATABASE_URL\" ] || [ -n \"$DB_HOST\" ]; then flask db upgrade; else echo 'No database configured - skipping migrations'; fi && python run.py"]
