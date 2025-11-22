import subprocess
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
study_path = os.getenv("STUDY_PATH", r"C:\Users\james\study\certs\aws\associate_dev")
vscode_path = os.getenv("VSCODE_PATH", "code")

# Check if directory exists
if not os.path.exists(study_path):
    print(f"Error: Directory not found at {study_path}")
    sys.exit(1)

# Navigate to directory and open VS Code
try:
    print(f"Opening VS Code in: {study_path}")
    subprocess.Popen([vscode_path, study_path])
    print("VS Code opened successfully!")
except FileNotFoundError:
    print(f"Error: VS Code not found at '{vscode_path}'")
    print("Make sure VS Code is installed and the path is correct in your .env file")
except Exception as e:
    print(f"Error opening VS Code: {e}")
