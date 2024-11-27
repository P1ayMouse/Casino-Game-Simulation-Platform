FROM python:3.9-slim

WORKDIR /app

COPY gateway/ /app/
COPY requirements.txt /app/

RUN mkdir -p /app/logs

RUN pip install --no-cache-dir -r requirements.txt

# Gunicorn для запуску додатку
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
