import time
import csv
import psutil
import datetime
import os

LOG_FILE = "usage_log.csv"

def get_active_window_title():
    try:
        import win32gui
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except:
        return "Unknown"

def log_usage():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'app'])

    while True:
        title = get_active_window_title()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, title])

        time.sleep(5)  # Log every 5 seconds

if __name__ == "__main__":
    log_usage()
