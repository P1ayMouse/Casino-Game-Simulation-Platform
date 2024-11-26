import random
import sys

def play_slot_game(stake):
    # Predefined constant distribution array with 50 different values plus 40 additional 0.0 multipliers
    distribution = [10.5, 0.0, 100.0, 5.3, 20.8, 0.1, 15.6, 50.0, 1.2, 200.0,
                    3.7, 500.0, 8.9, 30.0, 0.5, 60.0, 90.0, 7.5, 0.8, 300.0,
                    25.0, 12.4, 45.6, 0.2, 75.0, 2.5, 400.0, 6.1, 11.0, 250.0,
                    18.0, 4.0, 35.5, 80.0, 0.3, 9.0, 0.7, 150.0, 70.0, 0.4,
                    110.0, 5.0, 22.2, 13.3, 0.6, 175.0, 65.0, 1.8, 99.9, 14.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    # Select a random index from the distribution array
    multiplier = random.choice(distribution)
    win_amount = stake * multiplier
    return win_amount

def main():
    try:
       # Get stake from the command line argument
        if len(sys.argv) != 3:
            return
        stake = float(sys.argv[1])
        if stake <= 0:
            return
        
        # Calculate the win amount for 
        #rtp = sum(play_slot_game(1) for _ in range(number_of_rounds)) / number_of_rounds
        win = play_slot_game(1)

        print(f"{win:.2f}")
    except ValueError:
        return

if __name__ == "__main__":
    main()
