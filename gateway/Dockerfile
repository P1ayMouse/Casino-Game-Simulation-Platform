FROM python:3.9-slim

WORKDIR /app

COPY gateway/app.py /app/
COPY gateway/config/ /app/config/
COPY requirements.txt /app/

# Create logs directory
RUN mkdir -p /app/logs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
