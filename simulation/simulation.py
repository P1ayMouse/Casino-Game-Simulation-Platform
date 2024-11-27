import os
import sys
import subprocess
import psycopg2
import psycopg2.extras
import json
import logging
import yaml
import time
from multiprocessing import Pool, cpu_count
from datetime import datetime

# Завантаження конфігурації
with open('config/simulation_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

logging.basicConfig(
    filename='logs/simulation.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

DATABASE_CONFIG = config['database']


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


def simulate_spins(num_spins, stake, batch_size=10000):
    server_instance_id = os.getenv('SERVER_INSTANCE_ID', 'simulation_node')

    # Час початку симуляції
    simulation_start_time = time.perf_counter()
    start_timestamp = datetime.now()
    logging.info(f"Simulation start time: {start_timestamp}")

    results = []
    # Паралельні спіни
    with Pool(cpu_count()) as pool:
        spin_results = pool.imap_unordered(run_game_server, [stake] * num_spins)
        for idx, res in enumerate(spin_results, 1):
            if res and 'win_amount' in res:
                win_amount = res['win_amount']
                results.append((datetime.now(), win_amount, server_instance_id))
            else:
                logging.error("Invalid result from game server")

            if idx % batch_size == 0 or idx == num_spins:
                insert_many_into_db(results)
                results.clear()

    simulation_end_time = time.perf_counter()
    end_timestamp = datetime.now()
    logging.info(f"Simulation end time: {end_timestamp}")

    # Розрахунок тривалості симуляції
    simulation_duration = simulation_end_time - simulation_start_time
    logging.info(f"Calculated simulation duration: {simulation_duration} seconds")

    print(f"Simulation duration: {simulation_duration} seconds")

    # Збереження інформації про симуляцію
    insert_simulation_info(server_instance_id, start_timestamp, end_timestamp, simulation_duration, num_spins)


def insert_many_into_db(data):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO spin_results (timestamp, win_amount, server_instance_id) VALUES %s",
            data
        )
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Inserted {len(data)} records into DB")
    except Exception as e:
        logging.exception("Database error during batch insert")


def insert_simulation_info(instance_id, start_time, end_time, duration, num_spins):
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO simulation_info (instance_id, start_time, end_time, duration_seconds, num_spins)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (instance_id, start_time, end_time, duration, num_spins)
        )
        conn.commit()
        cur.close()
        conn.close()
        logging.info(f"Inserted simulation info for {instance_id} into DB")
    except Exception as e:
        logging.exception("Database error during inserting simulation info")
        print(f"Exception occurred during insert_simulation_info: {e}")


if __name__ == '__main__':
    num_spins = int(os.getenv('NUM_SPINS', '1000'))
    stake = float(os.getenv('STAKE', '1.0'))
    logging.info(f"Starting simulation with {num_spins} spins at stake {stake}")
    simulate_spins(num_spins, stake)
    logging.info("Simulation complete. Exiting.")
