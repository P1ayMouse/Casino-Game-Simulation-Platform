import random
import sys
import json
import logging

logging.basicConfig(
    filename='logs/game_server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)


def play_slot_game(stake):
    distribution = [10.5, 0.0, 10.0, 5.3, 2.8, 0.1, 5.6, 5.0, 1.2, 2.0,
                    3.7, 5.0, 8.9, 3.0, 0.5, 6.0, 9.0, 7.5, 0.8, 3.0,
                    5.0, 2.4, 5.6, 0.2, 7.0, 2.5, 4.0, 6.1, 11.0, 2.0,
                    8.0, 4.0, 5.5, 8.0, 0.3, 9.0, 0.7, 5.0, 7.0, 0.4,
                    10.0, 5.0, 2.2, 3.3, 0.6, 5.0, 6.0, 1.8, 9.9, 1.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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