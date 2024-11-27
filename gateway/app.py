import os
import sys
import yaml
import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import docker
import threading
import psycopg2

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

# Ініціалізація Docker клієнта
docker_client = docker.from_env()

# Параметри бази даних
DATABASE_CONFIG = config['database']

# Порт Simulation Nodes
SIMULATION_PORT = config.get('simulation_port', 5001)

# Глобальна змінна для збереження результатів
simulation_results = {}

simulation_in_progress = False


@app.route('/', methods=['GET', 'POST'])
def index():
    global simulation_results, simulation_in_progress
    if request.method == 'POST':
        num_spins = int(request.form.get('num_spins', 1000))
        stake = float(request.form.get('stake', 1.0))
        num_nodes = int(request.form.get('num_nodes', 2))

        # Запускаємо симуляцію
        response = start_simulation_request(num_spins, stake, num_nodes)
        message = response.get('status')

        # Встановлюємо статус симуляції в True
        simulation_in_progress = True

        return render_template('index.html', message=message)
    else:
        message = None
        if simulation_in_progress:
            message = "Симуляція запущена. Результати з'являться після завершення."
        return render_template('index.html', results=simulation_results, message=message)


def start_simulation_request(num_spins, stake, num_nodes):
    logging.info(f"Received simulation request: num_spins={num_spins}, stake={stake}, num_nodes={num_nodes}")

    # Розрахунок кількості спінів для кожного вузла
    spins_per_node = num_spins // num_nodes
    extra_spins = num_spins % num_nodes

    simulation_nodes = []

    # Створення та запуск Simulation Nodes
    for i in range(num_nodes):
        node_name = f"simulation_node_{i+1}"
        spins = spins_per_node + (1 if i < extra_spins else 0)

        logging.info(f"Creating container: {node_name} with {spins} spins")

        # Створення контейнера
        container = docker_client.containers.run(
            image='casino-game-simulation-platform_simulation_node',  # Ім'я образу Simulation Node
            name=node_name,
            environment={
                'SERVER_INSTANCE_ID': node_name,
                'NUM_SPINS': str(spins),
                'STAKE': str(stake)
            },
            detach=True,
            network='casino-game-simulation-platform_default',  # Мережа Docker Compose
            volumes={
                '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
                os.path.abspath('./logs'): {'bind': '/app/logs', 'mode': 'rw'}
            }
        )
        simulation_nodes.append(container)

    # Моніторинг контейнерів
    threading.Thread(target=monitor_containers, args=(simulation_nodes,)).start()

    return {"status": "Симуляція запущена. Результати з'являться після завершення."}


def monitor_containers(containers):
    global simulation_in_progress
    for container in containers:
        container.wait()  # Очікуємо завершення контейнера
        logging.info(f"Container {container.name} has exited.")
        container.remove()  # Видаляємо контейнер
        logging.info(f"Container {container.name} has been removed.")

    # Після завершення всіх контейнерів оновлюємо результати
    update_simulation_results()

    # Встановлюємо статус симуляції в False
    simulation_in_progress = False


def update_simulation_results():
    global simulation_results
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) AS total_spins,
                   SUM(win_amount) AS total_wins,
                   AVG(win_amount) AS average_win_per_spin
            FROM spin_results;
        """)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        simulation_results = {
            'total_spins': result[0],
            'total_wins': round(result[1], 2) if result[1] else 0.0,
            'average_win_per_spin': round(result[2], 4) if result[2] else 0.0
        }

        logging.info(f"Simulation results updated: {simulation_results}")
    except Exception as e:
        logging.exception("Error fetching simulation results")


@app.route('/check_status')
def check_status():
    global simulation_results, simulation_in_progress
    if simulation_in_progress:
        status = 'in_progress'
    else:
        status = 'completed'

    return jsonify({
        'status': status,
        'results': simulation_results
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['gateway_port'])
