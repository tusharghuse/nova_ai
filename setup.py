import subprocess
import sys
import os

def main():
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Installation failed.")

    os.makedirs("data", exist_ok=True)
    print("Setup complete.")

if __name__ == "__main__":
    main()