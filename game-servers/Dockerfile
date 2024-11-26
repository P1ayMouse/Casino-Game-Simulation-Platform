FROM python:3.9-slim

WORKDIR /app

COPY game-server.py /app/
COPY requirements.txt /app/
COPY logs/ /app/logs/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "game-server.py", "1.0"]
