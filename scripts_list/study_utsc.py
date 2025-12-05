import os
import sys
from dotenv import load_dotenv

# Add the parent directory (py_scripts) to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from template.study_template import StudyEnvironment


class CurrentStudy(StudyEnvironment):
    """Current study environment implementation"""

    def __init__(self, env_file=".env"):
        super().__init__(env_file)
        self.study_path_env = os.getenv("STUDY_UTSC")

        if not self.study_path_env:
            print("Error: STUDY_UTSC not found in .env file")
            exit(1)

    def get_study_path(self):
        """Return the current study path from environment"""
        return self.study_path_env


if __name__ == "__main__":
    # Create and launch the study environment
    study = CurrentStudy()
    study.launch()
    study.open_file_explorer(study.get_study_path())
