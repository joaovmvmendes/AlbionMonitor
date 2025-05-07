import json
import os
import logging
from typing import Dict, Any
from config.settings import STATE_FILE_PATH as STATE_FILE

logger = logging.getLogger(__name__)

def load_last_state() -> Dict[str, Any]:
    """
    Loads the last saved state from the local state file.

    Returns:
        dict: The last known state, or an empty dict if unavailable or corrupt.
    """
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read last state file '{STATE_FILE}': {e}")
    return {}

def save_current_state(data: Dict[str, Any]) -> None:
    """
    Saves the current state to the local state file.

    Parameters:
        data (dict): Dictionary representing the current state to persist.
    """
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(data, f)
    except IOError as e:
        logger.warning(f"Failed to write state file '{STATE_FILE}': {e}")