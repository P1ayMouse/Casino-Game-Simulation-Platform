import os
import sys
import yaml
import logging
from flask import Flask, request, jsonify
import requests

# Завантаження конфігурації
with open('config/gateway_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Налаштування логування
logging.basicConfig(
    filename='logs/gateway.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

app = Flask(__name__)

SIMULATION_NODES = config['simulation_nodes']

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    data = request.get_json()
    num_spins = data.get('num_spins', 1000)
    stake = data.get('stake', 1.0)

    for node in SIMULATION_NODES:
        try:
            response = requests.post(f"http://{node['host']}:{node['port']}/run_simulation", json={
                "num_spins": num_spins,
                "stake": stake
            })
            if response.status_code == 200:
                logging.info(f"Simulation started on node {node['host']}:{node['port']}")
            else:
                logging.error(f"Failed to start simulation on node {node['host']}:{node['port']}")
        except Exception as e:
            logging.exception(f"Error contacting simulation node {node['host']}:{node['port']}")

    return jsonify({"status": "Simulations started"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['gateway_port'])
