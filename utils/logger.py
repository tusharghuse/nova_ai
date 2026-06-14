"""
utils/logger.py
===============
Simple file logger. Writes timestamped entries to data/nova_ai.log.
"""

import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "nova_ai.log")


def log(message: str):
    """Append a timestamped message to the log file."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line)
    except Exception:
        pass  # Never crash the app because of a logging failure