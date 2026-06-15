"""core/assistant.py"""

import os
import re
import ollama

from core.voice import Voice
from modules.task_manager import TaskManager
from modules.scheduler import ReminderScheduler
from modules.system_actions import SystemActions
from modules.memory import Memory
from utils.logger import log
from utils.helpers import extract_time_from_text

SYSTEM_PROMPT = """
You are Nova AI, an advanced, highly capable AI personal assistant and productivity coach.

Your personality:
- You are a fully-fledged AI assistant. You can solve general queries, explain concepts, write code, and engage in normal conversation.
- You provide detailed, comprehensive, helpful, and friendly answers to any questions the user asks. Do not give overly short responses.
- When it comes to productivity, you are direct and action-oriented. You encourage the user to tackle their tasks.
- If the user asks for motivation, you provide it. You are supportive but firm about getting work done.

Rules you enforce:
1. Provide accurate and thorough answers to user queries.
2. If the user mentions their tasks or schedule, encourage them to take action.
3. Keep the conversation natural and conversational.
4. **Formatting:** Always structure your responses using a mix of short paragraphs and bullet points. Avoid long, unbroken walls of text. Provide well-structured and detailed explanations rather than brief, single-sentence answers.

Available commands the user can say or type:
- "add task [name]"         → adds a task
- "show tasks"              → lists all tasks
- "done task [number]"      → marks task complete
- "delete task [number]"    → removes a task
- "remind me at [time]"     → sets a reminder
- "open [app name]"         → opens an application
- "my goal is [goal]"       → saves a goal to memory
- "what is my goal"         → recalls saved goal
- "schedule my day"         → creates a time-blocked plan
- "help"                    → shows all commands
- "quit" or "goodbye"       → exits Nova AI
"""

class Assistant:
    def __init__(self, text_mode=False, web_mode=False):
        self.text_mode = text_mode
        self.web_mode  = web_mode
        self.voice     = Voice(text_mode=text_mode, web_mode=web_mode)
        self.tasks     = TaskManager()
        self.scheduler = ReminderScheduler(self.voice)
        self.system    = SystemActions()
        self.memory    = Memory()
        
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.scheduler.start()

    def start(self):
        greeting = self._build_greeting()
        self.voice.speak(greeting)

        while True:
            user_input = self.voice.listen()
            if not user_input:
                continue

            log(f"User: {user_input}")

            if any(w in user_input.lower() for w in ["quit", "exit", "goodbye", "bye"]):
                self.voice.speak("Session over. No excuses tomorrow. Get it done.")
                break

            if self._handle_command(user_input):
                continue

            response = self._chat(user_input)
            self.voice.speak(response)

    def process_input(self, text: str):
        log(f"User: {text}")
        if any(w in text.lower() for w in ["quit", "exit", "goodbye", "bye"]):
            self.voice.speak("Session over. No excuses tomorrow. Get it done.")
            return
            
        if self._handle_command(text):
            return

        response = self._chat(text)
        self.voice.speak(response)

    def get_messages(self):
        return self.voice.get_messages()

    def _build_greeting(self):
        goal = self.memory.get("goal")
        task_count = len(self.tasks.get_pending())

        base = f"Nova AI online. Your goal is: {goal}. " if goal else "Nova AI online. "
        if task_count == 0:
            base += "Ready when you are."
        else:
            base += f"You have {task_count} pending tasks. No excuses. Let's get moving."
        return base

    def _handle_command(self, text: str) -> bool:
        t = text.lower().strip()

        if t == "help":
            self.voice.speak(
                "Commands: add task, show tasks, done task [number], "
                "delete task [number], remind me at [time], open [app], "
                "my goal is [goal], what is my goal, schedule my day, quit."
            )
            return True

        if t.startswith("add task"):
            task_name = text[8:].strip()
            if task_name:
                self.tasks.add(task_name)
                self.voice.speak(f"Task added: {task_name}. Now stop planning and start doing.")
            else:
                self.voice.speak("You need to give the task a name.")
            return True

        if any(cmd in t for cmd in ["show tasks", "list tasks", "my tasks"]):
            pending = self.tasks.get_pending()
            if not pending:
                self.voice.speak("No pending tasks. Add tasks with 'add task [name]'.")
            else:
                lines = [f"{i+1}. {task['name']}" for i, task in enumerate(pending)]
                self.voice.speak("Your tasks: " + ", ".join(lines))
            return True

        if t.startswith("done task"):
            num = self._extract_number(t)
            if num:
                result = self.tasks.complete(num - 1)
                self.voice.speak(result)
            else:
                self.voice.speak("Tell me which task number to mark done.")
            return True

        if t.startswith("delete task"):
            num = self._extract_number(t)
            if num:
                result = self.tasks.delete(num - 1)
                self.voice.speak(result)
            else:
                self.voice.speak("Tell me which task number to delete.")
            return True

        if "remind me" in t:
            time_str, label = extract_time_from_text(text)
            if time_str:
                self.scheduler.add_reminder(time_str, label)
                self.voice.speak(f"Reminder set for {time_str}: {label}.")
            else:
                self.voice.speak("I couldn't read the time. Say something like: remind me at 5 PM to take a break.")
            return True

        if t.startswith("open "):
            app = text[5:].strip()
            result = self.system.open_app(app)
            self.voice.speak(result)
            return True

        if "my goal is" in t:
            goal_text = re.sub(r"my goal is", "", text, flags=re.IGNORECASE).strip()
            self.memory.set("goal", goal_text)
            self.voice.speak(f"Goal saved: {goal_text}. Now build a plan and execute it — today.")
            return True

        if any(cmd in t for cmd in ["what is my goal", "my goal"]):
            goal = self.memory.get("goal")
            if goal:
                self.voice.speak(f"Your goal is: {goal}. Are you working toward it right now?")
            else:
                self.voice.speak("No goal saved. Tell me your goal with: my goal is [goal].")
            return True

        if any(cmd in t for cmd in ["schedule my day", "plan my day"]):
            tasks = self.tasks.get_pending()
            if tasks:
                task_list = ", ".join([tk["name"] for tk in tasks])
                prompt = f"Create a strict daily schedule for these tasks: {task_list}. Start from 8 AM. Be concise."
            else:
                prompt = "Create a generic strict daily productivity schedule from 8 AM to 10 PM for a focused person."
            response = self._chat(prompt)
            self.voice.speak(response)
            return True

        return False

    def _chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        try:
            model_name = os.getenv("OLLAMA_MODEL", "phi3")
            response = ollama.chat(model=model_name, messages=self.history)
            reply = response['message']['content'].strip()
        except Exception as e:
            log(f"Ollama error: {e}")
            reply = f"API error: {str(e)}"

        self.history.append({"role": "assistant", "content": reply})

        if len(self.history) > 41:
            self.history = [self.history[0]] + self.history[-40:]

        log(f"Nova AI: {reply}")
        return reply

    def _extract_number(self, text: str):
        match = re.search(r"\d+", text)
        return int(match.group()) if match else None