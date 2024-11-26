import os
import requests
import psycopg2
from flask import Flask, request

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_simulation():
    data = request.get_json()
    filepath = data.get('filepath')

    if not filepath or not os.path.exists(filepath):
        return "File not found", 400

    # Print the content of the file to the console
    with open(filepath, 'r') as file:
        content = file.read()
        print(f"Content of the file {filepath}:\n{content}")

    # Store the result in the database
    conn = psycopg2.connect(
        dbname='simulation_results', user='user', password='password', host='database'
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO results (filepath, output) VALUES (%s, %s);", (filepath, content))
    conn.commit()
    cur.close()
    conn.close()

    return "Simulation complete", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)