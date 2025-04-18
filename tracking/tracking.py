from pynput import mouse, keyboard
import time
import math
import threading
import csv
from datetime import datetime

# Global variables
mouse_positions = []
key_presses = 0
tracking = True
start_time = time.time()
stop_key = "]"
pressed_keys = set()
csv_file = "tracking_data.csv"

# Initialize CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "APM", "Erratic Score", "Total Key Presses", "Total Mouse Movements"])

# Mouse listener
def on_move(x, y):
    global mouse_positions, tracking
    if not tracking:
        return
    current_time = time.time()
    mouse_positions.append((x, y, current_time))

def calculate_erratic_score():
    global mouse_positions
    distances = []
    time_deltas = []
    erratic_changes = 0

    for i in range(1, len(mouse_positions)):
        x1, y1, t1 = mouse_positions[i - 1]
        x2, y2, t2 = mouse_positions[i]

        # Calculate distance and time delta
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        time_delta = t2 - t1

        if time_delta > 0:
            speed = distance / time_delta
            if i > 1:  # Compare with the previous speed
                prev_speed = distances[-1] / time_deltas[-1]
                if abs(speed - prev_speed) > 100:  # Adjust threshold as needed
                    erratic_changes += 1

            distances.append(distance)
            time_deltas.append(time_delta)

    # Normalize erratic changes to a score between 0 and 1
    max_changes = len(mouse_positions)  # Maximum possible erratic changes
    erratic_score = erratic_changes / max_changes if max_changes > 0 else 0
    return erratic_score

# Keyboard listener
def on_press(key):
    global key_presses, pressed_keys
    # NOTE: we don't need pressed_keys unless we are trying to track which keys are pressed (delete later once decided)

    key_presses += 1

def on_release(key):
    if key == keyboard.Key.delete:
        return False

# Monitor APM and erratic score
def monitor_metrics():
    global start_time, key_presses, mouse_positions
    while True:
        time.sleep(10)

        elapsed_time = time.time() - start_time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # APM calculation
        apm = key_presses / (elapsed_time / 10)

        # Erratic movement calculation
        erratic_score = calculate_erratic_score()

        # Write metrics to CSV
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, f"{apm:.2f}", f"{erratic_score:.2f}", key_presses, len(mouse_positions)])

        print(f"Logged to CSV: {timestamp}, APM: {apm:.2f}, Erratic Score: {erratic_score:.2f}")

# Start monitoring metrics
monitor_thread = threading.Thread(target=monitor_metrics, daemon=True)
monitor_thread.start()

# create and start listeners 
with mouse.Listener(on_move=on_move) as listener:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()