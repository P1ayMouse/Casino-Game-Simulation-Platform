FROM python:3.9-slim

WORKDIR /app

COPY gateway/app.py /app/
COPY gateway/config/ /app/config/
COPY gateway/templates/ /app/templates/
COPY gateway/static/ /app/static/
COPY requirements.txt /app/

RUN mkdir -p /app/logs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
