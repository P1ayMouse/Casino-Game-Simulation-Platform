import random
import sys
import json
import logging

# Налаштування логування
logging.basicConfig(
    filename='logs/game_server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def play_slot_game(stake):
    # Розподіл множників
    distribution = [10.5, 0.0, 100.0, 5.3, 20.8, 0.1, 15.6, 50.0, 1.2, 200.0,
                    3.7, 500.0, 8.9, 30.0, 0.5, 60.0, 90.0, 7.5, 0.8, 300.0,
                    25.0, 12.4, 45.6, 0.2, 75.0, 2.5, 400.0, 6.1, 11.0, 250.0,
                    18.0, 4.0, 35.5, 80.0, 0.3, 9.0, 0.7, 150.0, 70.0, 0.4,
                    110.0, 5.0, 22.2, 13.3, 0.6, 175.0, 65.0, 1.8, 99.9, 14.0,
                    0.0] * 40  # Додаткові нулі

    multiplier = random.choice(distribution)
    win_amount = stake * multiplier
    return win_amount

def main():
    try:
        if len(sys.argv) != 2:
            logging.error("Invalid number of arguments.")
            print(json.dumps({"error": "Invalid number of arguments"}))
            sys.exit(1)
        stake = float(sys.argv[1])
        if stake <= 0:
            logging.error("Stake must be positive.")
            print(json.dumps({"error": "Stake must be positive"}))
            sys.exit(1)
        win = play_slot_game(stake)
        result = {
            "stake": stake,
            "win_amount": win
        }
        print(json.dumps(result))
        logging.info(f"Spin result: {result}")
    except ValueError:
        logging.exception("Invalid stake value.")
        print(json.dumps({"error": "Invalid stake value"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
