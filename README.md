![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# 🌌 Nova AI — On-Device AI Productivity Assistant

> 🏆 Built for **OSDHack 2026 — On Device AI Theme**
> 🧠 Fully local AI assistant powered by Ollama
> 🔒 Privacy-first • ⚡ Offline-capable • 🖥️ Desktop-native productivity system

---

<h3 align="center">🎬 Interactive Console Walkthrough</h3>
<p align="center">
  <video src="static/screenshots/demo.mp4" width="97%" controls autoplay loop muted></video>
</p>

<h3 align="center">🖥️ Interactive Dashboard Showcase</h3>
<p align="center">
  <img src="static/screenshots/dashboard.png" width="48%" alt="Nova AI Dashboard" />
  <img src="static/screenshots/open_app.png" width="48%" alt="Opening App Command" />
</p>
<p align="center">
  <img src="static/screenshots/completed_actions.png" width="97%" alt="Completed Actions & Productivity Hub" />
</p>

---

## 🚀 Overview

**Nova AI** is a local-first AI productivity assistant that runs entirely on the user's device and helps manage tasks, reminders, schedules, and system actions using natural language (text + voice).

Unlike cloud-based AI assistants, Nova AI is designed to operate **without sending user data to external APIs**, ensuring **privacy, speed, and offline usability**.

It combines:
* Local LLM inference (via Ollama)
* Voice interaction system
* Task + reminder engine
* OS-level automation
* Real-time productivity dashboard

---

## 🧠 Why Nova AI?

Modern AI assistants depend heavily on cloud APIs, which introduces:
* ❌ Privacy risks (user data leaves device)
* ❌ Internet dependency
* ❌ Latency issues
* ❌ API cost limitations

Nova AI demonstrates a different approach:
> ✅ AI that runs locally
> ✅ AI that respects privacy
> ✅ AI that works offline
> ✅ AI that acts like a real system assistant

---

## 🏆 OSDHack 2026 — On Device AI Alignment

Nova AI is built specifically for the **On Device AI** theme.

### 🧠 Core Requirement Fulfillment

| Requirement | Implementation |
| :--- | :--- |
| **On-device AI** | Ollama local LLM (phi3 / configurable models) |
| **Offline-first** | Core assistant works without internet |
| **Privacy-focused** | No cloud AI API calls |
| **Lightweight inference** | Runs on standard laptops |
| **Local execution** | All logic executed on user machine |

### 🌐 Cloud Usage (Optional Only)

Cloud services are NOT used for AI reasoning. They are only used for:
* Web UI hosting (Flask local server)
* Optional authentication or storage (future extension)

👉 **All intelligence stays on-device.**

---

## ⚡ Key Features

### 🧠 Local AI Engine
* Powered by **Ollama (phi3 or custom models)**
* Fully offline inference
* No external API dependency

### 🎙️ Voice + Text Interaction
* Speech-to-text input (local processing)
* Offline text-to-speech response system
* Dual-mode CLI + Web interaction

### 📅 Smart Task & Reminder System
* Add / complete / delete tasks
* Background scheduler for timed reminders
* Persistent local JSON storage

### 🖥️ Productivity Dashboard
* Live task tracking UI
* Goal management system
* Real-time productivity metrics

### 🛠️ System Automation
* Open applications via commands
* Cross-platform support (Windows, macOS, Linux)
* Native OS integration layer

### 🔒 Privacy-First Architecture
* No cloud AI inference
* No external prompt sharing
* Fully local memory storage

---

## 🏗️ System Architecture

```text
User Input (Text / Voice)
        ↓
Web UI / CLI Interface
        ↓
Assistant Core (Prompt Engine)
        ↓
Ollama Local LLM (On-device inference)
        ↓
------------------------------------------------
| Modules Layer                                 |
| - Task Manager (JSON storage)                 |
| - Scheduler (background reminders)            |
| - Memory System (local persistence)           |
| - System Actions (OS automation)              |
------------------------------------------------
```

---

## 📂 Project Structure

```text
Nova AI/
├── core/
│   ├── assistant.py        # AI core logic + system prompt
│   └── voice.py            # TTS + voice handling
├── modules/
│   ├── memory.py           # Local memory (JSON storage)
│   ├── scheduler.py        # Background reminder engine
│   ├── system_actions.py   # OS automation (open apps)
│   └── task_manager.py     # Task CRUD operations
├── static/
│   ├── app.js              # Frontend logic + API calls
│   └── index.css           # UI styling (glassmorphism)
├── templates/
│   └── index.html          # Dashboard UI
├── utils/
│   ├── helpers.py          # Time parsing utilities
│   └── logger.py           # Logging system
├── data/                  # Local dynamic JSON databases
│   ├── memory.json
│   ├── tasks.json
│   └── reminders.json
├── app.py                  # Flask server (Web mode)
├── main.py                 # CLI / Voice mode
├── requirements.txt
└── .env
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* Python 3.10+
* Ollama installed → [https://ollama.com/](https://ollama.com/)
* Pull a local model:
  ```bash
  ollama pull phi3
  ```

### 2. Clone Repository
```bash
git clone <repo-url>
cd nova-ai
```

### 3. Create Virtual Environment
```bash
python -m venv .venv
```
Activate:
* **Windows (PowerShell)**:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
* **Windows (CMD)**:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
* **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
> [!NOTE]
> If you are running the application in **Web Mode** (Flask server), you do not need `pyaudio` to build successfully. The web microphone uses `sounddevice` directly. If `pyaudio` fails to compile on Windows due to missing C++ compiler tools, you can ignore the error, as Flask mode will remain fully functional.

### 5. Environment Setup
Create a `.env` file in the root directory:
```env
OLLAMA_MODEL=phi3
GEMINI_API_KEY=your_optional_key
```

---

## ▶️ Running Nova AI

### 🖥️ Web Mode (Recommended)
```bash
python app.py
```
Open:
👉 **[http://localhost:5000](http://localhost:5000)**

* Chat interface
* Task management dashboard
* Voice input support
* Live productivity metrics

### 💻 CLI / Voice Mode
```bash
python main.py
```
Text-only mode:
```bash
python main.py --text
```

---

## 🗣️ Supported Commands

You can speak or type the following structured commands directly to Nova AI:

| Command | Action | Example |
| :--- | :--- | :--- |
| `add task [name]` | Create new task | *add task Finish presentation* |
| `show tasks` | List all tasks | *show tasks* |
| `done task [n]` | Mark task completed | *done task 1* |
| `delete task [n]` | Remove task | *delete task 2* |
| `my goal is [...]` | Set primary goal | *my goal is to build a startup* |
| `what is my goal` | View goal | *what is my goal* |
| `remind me at [time] [...]` | Schedule reminder | *remind me at 5:30 PM to drink water* |
| `open [app]` | Launch system app | *open vscode* |
| `schedule my day` | Generate daily plan | *schedule my day* |
| `help` | Show commands | *help* |
| `quit` / `goodbye` | Exit assistant | *quit* |

---

## 🛠️ Customization

### Configuring Application Shortcuts
To add new applications to the `open [app]` launcher command, edit the `APP_MAP` dict in [modules/system_actions.py](file:///d:/Projects/Nova%20AI/modules/system_actions.py):

```python
APP_MAP = {
    "chrome":  {"windows": "chrome", "darwin": "Google Chrome", "linux": "google-chrome"},
    # Add your own app configurations here...
}
```

### Modifying the AI Personality
To alter the demeanor or specific prompts of the coach, update the `SYSTEM_PROMPT` inside [core/assistant.py](file:///d:/Projects/Nova%20AI/core/assistant.py).

---

## 🧩 Use Cases
* Personal productivity assistant
* Offline AI chatbot
* Voice-controlled task manager
* Local automation system
* Privacy-focused AI alternative to cloud assistants

---

## 🚧 Future Improvements
* 🔌 Plugin system for custom tools
* 📱 Mobile companion app
* 🧠 Long-term vector memory (RAG upgrade)
* 📅 Google Calendar integration
* 🤖 Multi-agent task execution system
* 🎯 Smart prioritization engine

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and build upon this project with proper attribution.

See the full license details in the [LICENSE](./LICENSE) file.

---

## 👨‍💻 Author

Built by **Tushar Ghuse**

---

## 🏁 Final Note

Nova AI is designed to demonstrate a simple but powerful idea:
> “AI should run where the user is — not in the cloud.”
