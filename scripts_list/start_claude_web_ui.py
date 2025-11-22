import webbrowser
import subprocess
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Open Claude.ai in the default browser
print("Opening Claude.ai...")
webbrowser.open("https://claude.ai/new")

# Get VS Code parameters from environment variables
vscode_path = os.getenv("VSCODE_PATH", "code")  # Default to 'code' if not specified
vscode_workspace = os.getenv(
    "VSCODE_WORKSPACE", ""
)  # Optional workspace/folder to open

# Open VS Code
try:
    print("Opening VS Code...")
    if vscode_workspace:
        # Open VS Code with a specific workspace/folder
        subprocess.Popen([vscode_path, vscode_workspace])
        print(f"VS Code opened with: {vscode_workspace}")
    else:
        # Open VS Code without a specific workspace
        subprocess.Popen([vscode_path])
        print("VS Code opened")
except FileNotFoundError:
    print(f"Error: VS Code not found at '{vscode_path}'")
    print("Make sure VS Code is installed and the path is correct in your .env file")
except Exception as e:
    print(f"Error opening VS Code: {e}")

print("\nAll applications launched successfully!")
