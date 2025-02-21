from pynput import keyboard
import time
import csv
from datetime import datetime

csv_file = "timestamp_data.csv"
events = {'1': 'Game Start', '2': 'Key Event', '3': 'Game End'}

with open(csv_file, mode='w', newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Event'])

def write_to_file(key):
    print('in function')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, events[key]])

    print(f"Logged to CSV: {timestamp}, Event: {events[key]}")

def on_press(key):
    try:
        if key.char in events:
            print('in loop')
            write_to_file(key.char)
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.delete:
        return False
    
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()