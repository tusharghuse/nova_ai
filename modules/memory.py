import json
import os
from utils.logger import log

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "memory.json")

class Memory:
    def __init__(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
            self._save({})

    def set(self, key: str, value):
        data = self._load()
        data[key] = value
        self._save(data)
        log(f"Memory saved: {key} = {value}")

    def get(self, key: str, default=None):
        return self._load().get(key, default)

    def delete(self, key: str):
        data = self._load()
        if key in data:
            del data[key]
            self._save(data)

    def all(self) -> dict:
        return self._load()

    def _load(self) -> dict:
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save(self, data: dict):
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)