import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get file path from environment variable
file_path = os.getenv("YEARLY_PLANNING_PATH")

if not file_path:
    print("Error: YEARLY_PLANNING_PATH not found in .env file")
    sys.exit(1)

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

# Open the file with the default application
try:
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", file_path])
    else:  # Linux
        subprocess.run(["xdg-open", file_path])

    print(f"Opening: {file_path}")
except Exception as e:
    print(f"Error opening file: {e}")
