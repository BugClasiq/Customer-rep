FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Apply migrations, then serve on $PORT (Railway/Render inject PORT; default 5000 locally).
CMD ["sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:${PORT:-5000} run:app"]
