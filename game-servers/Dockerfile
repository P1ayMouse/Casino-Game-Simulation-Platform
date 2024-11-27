FROM python:3.9-slim

WORKDIR /app

COPY game-servers/game-server.py /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "game-server.py"]
