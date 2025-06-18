import random
import keyboard
import os
import sys

def check_root_permission():
    if os.name == 'posix':
        if os.geteuid() != 0:
            print("⚠️ This script requires root permissions to capture keyboard events on Linux.")
            print("💡 Please run as root or use sudo:")
            print(f"   sudo python3 {sys.argv[0]}")
            sys.exit(1)

def load_config(filename="config.txt"):
    config = {'currency_prefix': '$', 'check_duplicates': 'false', 'generate_hotkey': 'f9'}  # defaults
    if not os.path.isfile(filename):
        print("⚠️ config.txt not found. Using defaults.")
        return config
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
    return config

def check_duplicates_in_list(data, filename):
    duplicates = set([x for x in data if data.count(x) > 1])
    if duplicates:
        print(f"⚠️ Warning: Duplicate values found in {filename}: {duplicates}")

def load_slots(filename="slots.txt", check_duplicates=False):
    if not os.path.isfile(filename):
        print(f"Error: {filename} not found.")
        return []
    with open(filename, 'r') as f:
        slots = [line.strip() for line in f if line.strip()]
    if check_duplicates:
        check_duplicates_in_list(slots, filename)
    return slots

def load_weighted_values(filename, check_duplicates=False):
    if not os.path.isfile(filename):
        print(f"Error: {filename} not found.")
        return [], []
    values, weights = [], []
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                try:
                    value_str, weight_str = line.strip().split('=')
                    value = int(value_str.strip())
                    weight = int(weight_str.strip())
                    values.append(value)
                    weights.append(weight)
                except ValueError:
                    print(f"Skipping invalid line in {filename}: {line}")
    if check_duplicates:
        check_duplicates_in_list(values, filename)
    return values, weights

def generate_spin_bet_slot(slots, spin_data, bet_data, currency_prefix):
    spin_counts, spin_weights = spin_data
    bet_sizes, bet_weights = bet_data

    if not slots:
        print("Error: No slots loaded.")
        return

    spin = random.choices(spin_counts, weights=spin_weights, k=1)[0]
    bet = random.choices(bet_sizes, weights=bet_weights, k=1)[0]
    slot = random.choice(slots)

    print(f"🎰 Slot: {slot} | Spin Count: {spin} | 💰 Bet Size: {currency_prefix}{bet:.2f}")

def main():
    check_root_permission()
    config = load_config()

    check_duplicates = config.get('check_duplicates', 'false').lower() == 'true'
    currency_prefix = config.get('currency_prefix', '$')
    generate_hotkey = config.get('generate_hotkey', 'f9').lower()

    slots = load_slots("slots.txt", check_duplicates)
    spin_data = load_weighted_values("spincount.txt", check_duplicates)
    bet_data = load_weighted_values("bet.txt", check_duplicates)

    if not slots or not spin_data[0] or not bet_data[0]:
        print("Error loading one or more files. Exiting.")
        return

    print(f"Press {generate_hotkey.upper()} to generate a new slot/spin/bet... (ESC to exit)")
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting.")
                break
            elif event.name == generate_hotkey:
                generate_spin_bet_slot(slots, spin_data, bet_data, currency_prefix)

if __name__ == "__main__":
    main()
