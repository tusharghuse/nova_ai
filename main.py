import argparse
import sys
from core.assistant import Assistant
from utils.logger import log

def main():
    parser = argparse.ArgumentParser(description="Nova AI Assistant")
    parser.add_argument(
        "--text",
        action="store_true",
        help="Run in text-only mode"
    )
    args = parser.parse_args()

    print("=" * 55)
    print(" Nova AI Assistant Started")
    print("=" * 55)

    try:
        assistant = Assistant(text_mode=args.text)
        assistant.start()
    except KeyboardInterrupt:
        log("Session ended by user (Ctrl+C).")
        print("\n\n[Nova AI] Session ended.")
        sys.exit(0)

if __name__ == "__main__":
    main()