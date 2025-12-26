import os
import sys
from dotenv import load_dotenv


# Add the parent directory (py_scripts) to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from template.coding_template import CodingEnvironment


class CurrentCoding(CodingEnvironment):
    """Current coding environment implementation"""

    def __init__(self, env_file=".env"):
        super().__init__(env_file)
        self.coding_path_env = os.getenv("CODING_SCRIPT_LAUNCHER")

        if not self.coding_path_env:
            print("Error: CODING_SCRIPT_LAUNCHER not found in .env file")
            exit(1)

    def get_coding_path(self):
        """Return the current coding path from environment"""
        return self.coding_path_env


if __name__ == "__main__":
    # Create and launch the coding environment
    coding = CurrentCoding()
    coding.launch()
    coding.open_powershell(coding.get_coding_path())
