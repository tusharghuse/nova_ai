import json
import os
import threading
import time
from datetime import datetime
from utils.logger import log

REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "reminders.json")

class ReminderScheduler:
    def __init__(self, voice):
        self.voice = voice
        self.running = False
        os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
        if not os.path.exists(REMINDERS_FILE):
            self._save([])

    def add_reminder(self, time_str: str, label: str):
        reminders = self._load()
        reminders.append({
            "time": time_str,
            "label": label if label else "Time's up!",
            "fired": False
        })
        self._save(reminders)
        log(f"Reminder added: {time_str} — {label}")

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()
        log("Reminder scheduler started.")

    def get_all(self) -> list:
        return self._load()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            self._check_reminders()
            time.sleep(30)

    def _check_reminders(self):
        now = datetime.now()
        now_str = now.strftime("%H:%M")
        reminders = self._load()
        changed = False

        for reminder in reminders:
            if reminder["fired"]:
                continue

            stored = self._normalise_time(reminder["time"])
            if stored == now_str:
                message = f"Reminder: {reminder['label']}"
                log(f"Firing reminder: {message}")
                self.voice.speak(message)
                reminder["fired"] = True
                changed = True

        if changed:
            self._save(reminders)

    def _normalise_time(self, time_str: str) -> str:
        time_str = time_str.strip().upper()
        for fmt in ("%I:%M %p", "%I %p", "%H:%M", "%I:%M%p", "%I%p"):
            try:
                return datetime.strptime(time_str, fmt).strftime("%H:%M")
            except ValueError:
                continue
        return time_str

    def _load(self) -> list:
        try:
            with open(REMINDERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self, reminders: list):
        with open(REMINDERS_FILE, "w") as f:
            json.dump(reminders, f, indent=2)
