import os
import sys
import subprocess
import psycopg2
import json
import logging
import yaml
from multiprocessing import Pool, cpu_count
from flask import Flask, request, jsonify
from datetime import datetime

# Завантаження конфігурації
with open('config/simulation_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Налаштування логування
logging.basicConfig(
    filename='logs/simulation.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

DATABASE_CONFIG = config['database']

app = Flask(__name__)

def run_game_server(stake):
    try:
        result = subprocess.run(['python', 'game-servers/game-server.py', str(stake)], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Game server error: {result.stderr}")
            return None
        else:
            return json.loads(result.stdout.strip())
    except Exception as e:
        logging.exception("Error running game server")
        return None

def insert_into_db(win_amount, server_instance_id):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO spin_results (timestamp, win_amount, server_instance_id) VALUES (%s, %s, %s);",
            (datetime.now(), win_amount, server_instance_id)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.exception("Database error")

def simulate_spins(num_spins, stake):
    server_instance_id = os.getenv('SERVER_INSTANCE_ID', 'simulation_node')
    with Pool(cpu_count()) as pool:
        results = pool.map(run_game_server, [stake]*num_spins)
    for res in results:
        if res and 'win_amount' in res:
            win_amount = res['win_amount']
            insert_into_db(win_amount, server_instance_id)
            logging.info(f"Inserted win amount {win_amount} into DB")
        else:
            logging.error("Invalid result from game server")

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    data = request.get_json()
    num_spins = data.get('num_spins', 1000)
    stake = data.get('stake', 1.0)

    logging.info(f"Starting simulation with {num_spins} spins at stake {stake}")
    simulate_spins(num_spins, stake)
    return jsonify({"status": "Simulation complete"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['simulation_port'])
