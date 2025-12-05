import subprocess
import os
import sys
from dotenv import load_dotenv
from abc import ABC, abstractmethod


class StudyEnvironment(ABC):
    """Abstract base class for study environment setup"""

    def __init__(self, env_file=".env"):
        """Initialize and load environment variables"""
        load_dotenv(env_file)
        self.vscode_path = os.getenv("VSCODE_PATH", "code")

    @abstractmethod
    def get_study_path(self):
        """Return the study path - must be implemented by subclasses"""
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

    def launch(self):
        """Main method to launch the study environment"""
        study_path = self.get_study_path()

        if not study_path:
            print("Error: Study path not configured")
            sys.exit(1)

        if not self.validate_path(study_path):
            sys.exit(1)

        if not self.open_vscode(study_path):
            sys.exit(1)
