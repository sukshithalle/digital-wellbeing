import time
import csv
import os
import json
from datetime import datetime
import win32gui
import psutil

CONFIG_FILE = "focus_config.json"
LOG_FILE = "usage_log.csv"

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def load_focus_config():
    if not os.path.exists(CONFIG_FILE):
        return {"focus_mode": False, "time_limits": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

site_times = {}
last_app = None
start_time = time.time()

while True:
    title = get_active_window_title()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "YouTube" in title:
        app = "YouTube"
        category = "Distracting"
    elif "WhatsApp" in title:
        app = "WhatsApp"
        category = "Distracting"
    elif "Visual Studio Code" in title:
        app = "VS Code"
        category = "Productive"
    elif "Gmail" in title:
        app = "Gmail"
        category = "Neutral"
    else:
        app = "Other"
        category = "Neutral"

    if app != last_app and last_app:
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, last_app, site_category, duration])
        site_times[last_app] = site_times.get(last_app, 0) + duration
        start_time = time.time()
        last_app = app
        site_category = category
    elif app == last_app:
        site_category = category

    config = load_focus_config()
    if config["focus_mode"]:
        limit = config["time_limits"].get(app, None)
        if limit and site_times.get(app, 0) > limit:
            print(f"⛔ Focus Mode: Blocking {app} (limit reached)")
            for proc in psutil.process_iter(['name']):
                if app.lower() in proc.info['name'].lower():
                    try:
                        proc.kill()
                        print(f"Killed {proc.info['name']}")
                    except:
                        pass

    time.sleep(1)
