import os
import platform
import subprocess
from utils.logger import log

APP_MAP = {
    "chrome":       {"windows": "chrome",       "darwin": "Google Chrome", "linux": "google-chrome"},
    "firefox":      {"windows": "firefox",      "darwin": "Firefox",       "linux": "firefox"},
    "edge":         {"windows": "msedge",       "darwin": "Microsoft Edge","linux": "microsoft-edge"},
    "notepad":      {"windows": "notepad",      "darwin": "TextEdit",      "linux": "gedit"},
    "vscode":       {"windows": "code",         "darwin": "Visual Studio Code", "linux": "code"},
    "word":         {"windows": "winword",      "darwin": "Microsoft Word","linux": "libreoffice --writer"},
    "excel":        {"windows": "excel",        "darwin": "Microsoft Excel","linux": "libreoffice --calc"},
    "powerpoint":   {"windows": "powerpnt",     "darwin": "Microsoft PowerPoint","linux": "libreoffice --impress"},
    "whatsapp":     {"windows": "WhatsApp",     "darwin": "WhatsApp",      "linux": "whatsapp-desktop"},
    "slack":        {"windows": "slack",        "darwin": "Slack",         "linux": "slack"},
    "zoom":         {"windows": "zoom",         "darwin": "zoom.us",       "linux": "zoom"},
    "terminal":     {"windows": "cmd",          "darwin": "Terminal",      "linux": "gnome-terminal"},
    "calculator":   {"windows": "calc",         "darwin": "Calculator",    "linux": "gnome-calculator"},
    "files":        {"windows": "explorer",     "darwin": "Finder",        "linux": "nautilus"},
    "spotify":      {"windows": "spotify",      "darwin": "Spotify",       "linux": "spotify"},
}

class SystemActions:
    def __init__(self):
        self.os_name = platform.system().lower()

    def open_app(self, app_name: str) -> str:
        key = app_name.lower().strip()

        if key not in APP_MAP:
            return (
                f"I don't have '{app_name}' in my list. "
                "You can add it in modules/system_actions.py under APP_MAP."
            )

        os_key = "darwin" if "darwin" in self.os_name else (
                 "windows" if "windows" in self.os_name else "linux")

        cmd = APP_MAP[key].get(os_key)
        if not cmd:
            return f"No command configured for {app_name} on {self.os_name}."

        try:
            if "darwin" in self.os_name:
                subprocess.Popen(["open", "-a", cmd])
            elif "windows" in self.os_name:
                subprocess.Popen(["start", cmd], shell=True)
            else:
                subprocess.Popen([cmd], shell=True)

            log(f"Opened app: {app_name}")
            return f"Opening {app_name}. Stay focused — no distractions."

        except FileNotFoundError:
            return f"Could not find {app_name}. Make sure it's installed."
        except Exception as e:
            log(f"Error opening {app_name}: {e}")
            return f"Failed to open {app_name}."