import random
import keyboard
import os
import sys
import atexit
import urllib.request

picked_file_path = "picked.txt"

def check_root_permission():
    if os.name == 'posix':
        if os.geteuid() != 0:
            print("⚠️ This script requires root permissions to capture keyboard events on Linux.")
            print("💡 Please run as root or use sudo:")
            print(f"   sudo python3 {sys.argv[0]}")
            sys.exit(1)

def load_config(filename="config.txt"):
    config = {
        'currency_prefix': '$',
        'check_duplicates': 'false',
        'generate_hotkey': 'f9',
        'enable_bet': 'true',
        'enable_spin_count': 'true',
        'track_picked_slots': 'false',
        'auto_update_slots': 'false',
        'slots_url': None
    }
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

def load_slots(filename="slots.txt", check_duplicates=False, auto_update=False, slots_url=None):
    if auto_update and slots_url:
        try:
            print("🌐 Fetching latest slots list from GitHub...")
            response = urllib.request.urlopen(slots_url, timeout=10)
            data = response.read().decode("utf-8")
            with open(filename, "w") as f:
                f.write(data)
            print("✅ Slots list updated from GitHub.")
        except Exception as e:
            print(f"⚠️ Failed to fetch slots from URL ({e}). Falling back to local {filename}.")

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
                    weight = float(weight_str.strip())  # decimal weights supported
                    values.append(value)
                    weights.append(weight)
                except ValueError:
                    print(f"Skipping invalid line in {filename}: {line}")
    if check_duplicates:
        check_duplicates_in_list(values, filename)
    return values, weights

def save_picked_slot(slot):
    with open(picked_file_path, 'a') as f:
        f.write(slot + '\n')

def load_picked_slots():
    if not os.path.exists(picked_file_path):
        return []
    with open(picked_file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def cleanup_picked_file():
    if os.path.exists(picked_file_path):
        os.remove(picked_file_path)

def generate_spin_bet_slot(slots, spin_data, bet_data, currency_prefix, enable_spin, enable_bet, track_picked):
    spin_counts, spin_weights = spin_data
    bet_sizes, bet_weights = bet_data

    if not slots:
        print("Error: No slots loaded.")
        return

    available_slots = slots
    if track_picked:
        picked = load_picked_slots()
        available_slots = [slot for slot in slots if slot not in picked]
        if not available_slots:
            print("✅ All slots have been picked. Resetting picked list.")
            cleanup_picked_file()
            available_slots = slots

    slot = random.choice(available_slots)
    if track_picked:
        save_picked_slot(slot)

    parts = [f"🎰 Slot: {slot}"]

    if enable_spin and spin_counts:
        spin = random.choices(spin_counts, weights=spin_weights, k=1)[0]
        parts.append(f"Spin Count: {spin}")

    if enable_bet and bet_sizes:
        bet = random.choices(bet_sizes, weights=bet_weights, k=1)[0]
        parts.append(f"💰 Bet Size: {currency_prefix}{bet:.2f}")

    print(" | ".join(parts))

def main():
    check_root_permission()
    config = load_config()

    check_duplicates = config.get('check_duplicates', 'false').lower() == 'true'
    currency_prefix = config.get('currency_prefix', '$')
    generate_hotkey = config.get('generate_hotkey', 'f9').lower()
    enable_spin = config.get('enable_spin_count', 'true').lower() == 'true'
    enable_bet = config.get('enable_bet', 'true').lower() == 'true'
    track_picked = config.get('track_picked_slots', 'false').lower() == 'true'
    auto_update_slots = config.get('auto_update_slots', 'false').lower() == 'true'
    slots_url = config.get('slots_url', None)

    slots = load_slots("slots.txt", check_duplicates, auto_update=auto_update_slots, slots_url=slots_url)
    spin_data = load_weighted_values("spincount.txt", check_duplicates)
    bet_data = load_weighted_values("bet.txt", check_duplicates)

    if not slots or (enable_spin and not spin_data[0]) or (enable_bet and not bet_data[0]):
        print("Error loading one or more files. Exiting.")
        return

    print(f"Press {generate_hotkey.upper()} to generate a new slot/spin/bet... (ESC to exit)")
    atexit.register(cleanup_picked_file)

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'esc':
                print("Exiting.")
                break
            elif event.name == generate_hotkey:
                generate_spin_bet_slot(slots, spin_data, bet_data, currency_prefix, enable_spin, enable_bet, track_picked)

if __name__ == "__main__":
    main()
