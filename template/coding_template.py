import subprocess
import os
import sys
from dotenv import load_dotenv
import webbrowser
import time
import json
from abc import ABC, abstractmethod


class CodingEnvironment(ABC):
    """Abstract base class for coding environment setup"""

    def __init__(self, env_file=".env"):
        """Initialize and load environment variables"""
        load_dotenv(env_file)
        self.vscode_path = os.getenv("VSCODE_PATH", "code")

    @abstractmethod
    def get_coding_path(self):
        """Return the coding path - must be implemented by subclasses"""
        pass

    def validate_path(self, path):
        """Check if the directory exists"""
        if not os.path.exists(path):
            print(f"Error: Directory not found at {path}")
            return False
        return True

    def open_vscode(self, path):
        """Open VS Code in the specified directory"""
        try:
            print(f"Opening VS Code in: {path}")
            subprocess.Popen([self.vscode_path, path])
            print("VS Code opened successfully!")
            return True
        except FileNotFoundError:
            print(f"Error: VS Code not found at '{self.vscode_path}'")
            print(
                "Make sure VS Code is installed and the path is correct in your .env file"
            )
            return False
        except Exception as e:
            print(f"Error opening VS Code: {e}")
            return False

    def open_file_explorer(self, path):
        """Open file explorer in the specified directory"""
        try:
            print(f"Opening File Explorer in: {path}")
            if sys.platform == "win32":
                subprocess.Popen(["explorer", path])
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", path])
            else:  # Linux
                subprocess.Popen(["xdg-open", path])
            print("File Explorer opened successfully!")
            return True
        except Exception as e:
            print(f"Error opening File Explorer: {e}")
            return False

    def open_websites(self, websites_array):
        websites_json = os.getenv(websites_array, "[]")
        websites = json.loads(websites_json)

        try:
            for url in websites:
                webbrowser.open(url)
                time.sleep(3)
            print("All websites opened successfully")
        except Exception as e:
            print(f"Error opening websites: {e}")

    def launch(self):
        """Main method to launch the coding environment"""
        coding_path = self.get_coding_path()

        if not coding_path:
            print("Error: coding path not configured")
            sys.exit(1)

        if not self.validate_path(coding_path):
            sys.exit(1)

        # auto-triggers vs code in rel path with check
        if not self.open_vscode(coding_path):
            sys.exit(1)

    def open_powershell(self, path):
        try:
            subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoExit",
                    "-ExecutionPolicy",
                    "Bypass",
                ],
                cwd=path,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            return True
        except Exception as e:
            print(f"Error opening PowerShell: {e}")
            return False
