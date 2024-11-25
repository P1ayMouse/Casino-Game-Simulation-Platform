-- Таблиця для збереження результатів окремих обертань
CREATE TABLE IF NOT EXISTS spin_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    win_amount NUMERIC NOT NULL,
    server_instance_id VARCHAR(50)
);

-- Таблиця для збереження зведеної статистики
CREATE TABLE IF NOT EXISTS summary_statistics (
    id SERIAL PRIMARY KEY,
    total_spins BIGINT DEFAULT 0,
    total_wins NUMERIC DEFAULT 0,
    average_win_per_spin NUMERIC DEFAULT 0
);
