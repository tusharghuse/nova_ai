import json
import os
from datetime import datetime
from utils.logger import log

TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")

class TaskManager:
    def __init__(self):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        if not os.path.exists(TASKS_FILE):
            self._save([])

    def add(self, name: str):
        tasks = self._load()
        new_id = max((t["id"] for t in tasks), default=0) + 1
        tasks.append({
            "id": new_id,
            "name": name,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self._save(tasks)
        log(f"Task added: {name}")

    def get_all(self) -> list:
        return self._load()

    def get_pending(self) -> list:
        return [t for t in self._load() if not t["done"]]

    def complete(self, index: int) -> str:
        tasks = self._load()
        pending = [t for t in tasks if not t["done"]]

        if index < 0 or index >= len(pending):
            return "Invalid task number."

        target_id = pending[index]["id"]
        for task in tasks:
            if task["id"] == target_id:
                task["done"] = True
                self._save(tasks)
                log(f"Task completed: {task['name']}")
                return f"Done: '{task['name']}'. Good. Keep the momentum."

        return "Task not found."

    def delete(self, index: int) -> str:
        tasks = self._load()
        pending = [t for t in tasks if not t["done"]]

        if index < 0 or index >= len(pending):
            return "Invalid task number."

        target_id = pending[index]["id"]
        name = next(t["name"] for t in tasks if t["id"] == target_id)
        tasks = [t for t in tasks if t["id"] != target_id]
        self._save(tasks)
        log(f"Task deleted: {name}")
        return f"Deleted: '{name}'."

    def _load(self) -> list:
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, tasks: list):
        with open(TASKS_FILE, "w") as f:
            json.dump(tasks, f, indent=2)