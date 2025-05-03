import json
import os
from config.settings import STATE_FILE_PATH as STATE_FILE

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_current_state(data):
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f)
