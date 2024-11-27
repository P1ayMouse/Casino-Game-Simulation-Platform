FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY simulation/simulation.py /app/
COPY simulation/config/ /app/config/
COPY requirements.txt /app/
COPY game-servers/ /app/game-servers/

RUN mkdir -p /app/logs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "simulation.py"]
