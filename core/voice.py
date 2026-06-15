import pyttsx3
import speech_recognition as sr
from utils.logger import log

class Voice:
    def __init__(self, text_mode=False, web_mode=False):
        self.text_mode = text_mode
        self.web_mode = web_mode
        self.web_messages = []
        self.recognizer = None if web_mode or text_mode else sr.Recognizer()
        self.engine = None

        if not self.text_mode and not self.web_mode:
            self._setup_tts()

    def _setup_tts(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 170)
            self.engine.setProperty("volume", 1.0)

            voices = self.engine.getProperty("voices")
            for voice in voices:
                if "zira" in voice.name.lower() or "female" in voice.name.lower():
                    self.engine.setProperty("voice", voice.id)
                    break
            else:
                for voice in voices:
                    if "english" in voice.name.lower() or "en" in voice.id.lower():
                        self.engine.setProperty("voice", voice.id)
                        break
        except Exception as e:
            self.engine = None
            log(f"TTS init error: {e}")

    def speak(self, text: str):
        print(f"\n[Nova AI] {text}\n")
        if self.web_mode:
            self.web_messages.append(text)
        if not self.text_mode and not self.web_mode and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                log(f"TTS error: {e}")

    def get_messages(self):
        msgs = self.web_messages[:]
        self.web_messages.clear()
        return msgs

    def listen(self) -> str:
        if self.web_mode:
            return ""

        if self.text_mode:
            try:
                raw = input("You: ").strip()
                return raw.lower()
            except EOFError:
                return "quit"

        print("[Listening...]")
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)

            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            log(f"Heard: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Didn't catch that. Say it again.")
            return ""
        except sr.RequestError as e:
            log(f"STT request error: {e}")
            self.speak("Speech service error. Switching to text input this turn.")
            try:
                raw = input("You (type): ").strip()
                return raw.lower()
            except Exception:
                return ""
        except Exception as e:
            log(f"Listen error: {e}")
            return ""
