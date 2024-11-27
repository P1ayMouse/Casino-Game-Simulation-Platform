CREATE TABLE simulation_info (
    id SERIAL PRIMARY KEY,
    instance_id VARCHAR(255),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds DOUBLE PRECISION,
    num_spins INTEGER
);

CREATE TABLE spin_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    win_amount DECIMAL,
    server_instance_id VARCHAR(255)
);
