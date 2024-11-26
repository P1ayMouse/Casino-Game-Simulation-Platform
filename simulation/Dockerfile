FROM python:3.9-slim

WORKDIR /app

COPY simulation/simulation.py /app/
COPY simulation/config/ /app/config/
COPY requirements.txt /app/
COPY game-servers/ /app/game-servers/

# Create logs directory inside the container
RUN mkdir -p /app/logs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "simulation.py"]
