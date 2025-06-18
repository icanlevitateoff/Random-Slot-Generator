import random
import keyboard
import os
import sys

def check_root_permission():
    if os.name == 'posix':  # This is Linux or Unix-like
        if os.geteuid() != 0:
            print("⚠️ This script requires root permissions to capture keyboard events on Linux.")
            print("💡 Please run this script as root or using sudo:")
            print(f"   sudo python3 {sys.argv[0]}")
            sys.exit(1)

def load_slots(filename="slots.txt"):
    if not os.path.isfile(filename):
        print(f"Error: {filename} not found.")
        return []
    with open(filename, 'r') as f:
        slots = [line.strip() for line in f if line.strip()]
    return slots

def load_weighted_values(filename):
    if not os.path.isfile(filename):
        print(f"Error: {filename} not found.")
        return [], []

    values, weights = [], []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                try:
                    value_str, weight_str = line.split('=')
                    value = int(value_str.strip())
                    weight = int(weight_str.strip())
                    values.append(value)
                    weights.append(weight)
                except ValueError:
                    print(f"Skipping invalid line in {filename}: {line}")
    return values, weights

def generate_spin_bet_slot(slots, spin_data, bet_data):
    spin_counts, spin_weights = spin_data
    bet_sizes, bet_weights = bet_data

    if not slots:
        print("Error: No slots loaded.")
        return

    spin = random.choices(spin_counts, weights=spin_weights, k=1)[0]
    bet = random.choices(bet_sizes, weights=bet_weights, k=1)[0]
    slot = random.choice(slots)

    print(f"🎰 Slot: {slot} | Spin Count: {spin} | 💰 Bet Size: ${bet:.2f}")

def main():
    check_root_permission()

    slots = load_slots("slots.txt")
    spin_data = load_weighted_values("spincount.txt")
    bet_data = load_weighted_values("bet.txt")

    if not slots or not spin_data[0] or not bet_data[0]:
        print("Error loading one or more files. Exiting.")
        return

    print("Press F9 to generate a new slot/spin/bet... (ESC to exit)")
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting.")
                break
            elif event.name == 'f9':
                generate_spin_bet_slot(slots, spin_data, bet_data)

if __name__ == "__main__":
    main()
