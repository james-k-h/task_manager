import webbrowser
import time
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get websites from environment variable and parse as JSON array
websites_json = os.getenv("WEBSITES", "[]")
websites = json.loads(websites_json)

if not websites:
    print("No websites found in .env file. Please check your configuration.")
    exit(1)

# Open each website in a new tab
for url in websites:
    webbrowser.open(url)
    time.sleep(1)  # Brief delay between opening tabs

print(f"Successfully opened {len(websites)} websites!")
