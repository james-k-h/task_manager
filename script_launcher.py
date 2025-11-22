import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from dotenv import load_dotenv
import json


class ScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Launcher")
        self.root.geometry("600x600")
        self.root.configure(bg="white")

        # Load environment variables
        load_dotenv()

        # Load scripts from environment variable
        self.scripts = self.load_scripts()

        # Current page
        self.current_page = None

        # Create main container
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Show navigation menu
        self.show_navigation()

    def load_scripts(self):
        """Load scripts list from environment variable"""
        try:
            scripts_json = os.getenv("SCRIPTS_LIST")

            if not scripts_json:
                print("ERROR: SCRIPTS_LIST not found in .env file")
                return {}

            # Parse JSON string
            scripts_data = json.loads(scripts_json)

            # Validate structure
            if not isinstance(scripts_data, dict):
                print("ERROR: SCRIPTS_LIST must be a JSON object with categories")
                return {}

            return scripts_data

        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in SCRIPTS_LIST: {e}")
            return {}
        except Exception as e:
            print(f"ERROR: Failed to load scripts: {e}")
            return {}

    def show_navigation(self):
        """Display the navigation menu"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(
            self.main_frame,
            text="Script Launcher",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
        )
        title.pack(pady=14)

        # Subtitle
        subtitle = tk.Label(
            self.main_frame,
            text="Select a category",
            font=("Arial", 12),
            bg="white",
            fg="#333333",
        )
        subtitle.pack(pady=6)

        # Button frame
        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(pady=12, padx=30, fill="both", expand=True)

        # Navigation buttons
        categories = [
            ("Coding", "coding"),
            ("Finances", "finances"),
            ("Morning Activities", "morning"),
            ("Study", "study"),
        ]

        for display_name, category_key in categories:
            btn = tk.Button(
                button_frame,
                text=display_name,
                command=lambda cat=category_key, name=display_name: self.show_category(
                    cat, name
                ),
                bg="#d3d3d3",
                fg="black",
                font=("Arial", 14),
                width=20,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
            )
            btn.pack(pady=15)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#c0c0c0"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#d3d3d3"))

    def show_category(self, category, category_name):
        """Display scripts for a specific category"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_page = category

        # Header frame
        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=20, padx=20)

        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            command=self.show_navigation,
            bg="#e0e0e0",
            fg="black",
            font=("Arial", 10),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
        )
        back_btn.pack(side="left")
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#d0d0d0"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#e0e0e0"))

        # Category title
        title = tk.Label(
            header_frame,
            text=category_name,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black",
        )
        title.pack(side="left", padx=20)

        # Scripts frame
        scripts_frame = tk.Frame(self.main_frame, bg="white")
        scripts_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # Get scripts for this category
        category_scripts = self.scripts.get(category, [])

        if not category_scripts:
            error_label = tk.Label(
                scripts_frame,
                text=f"No scripts found for {category_name}\nPlease configure SCRIPTS_LIST in .env",
                font=("Arial", 11),
                bg="white",
                fg="#cc0000",
            )
            error_label.pack(pady=40)
            return

        # Create buttons for each script
        for script in category_scripts:
            script_name = script.get("name", "Unnamed Script")
            script_path = script.get("path", "")

            btn = tk.Button(
                scripts_frame,
                text=script_name,
                command=lambda name=script_name, path=script_path: self.run_script(
                    name, path
                ),
                bg="#d3d3d3",
                fg="black",
                font=("Arial", 11),
                width=35,
                height=2,
                relief="raised",
                borderwidth=2,
                cursor="hand2",
            )
            btn.pack(pady=8)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#c0c0c0"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#d3d3d3"))

    def run_script(self, script_name, script_path):
        """Execute the script and print status to PowerShell"""
        print(f"\n{'=' * 50}")
        print(f"Executing: {script_name}")
        print(f"Path: {script_path}")
        print(f"{'=' * 50}")

        try:
            # Check if script exists
            if not os.path.exists(script_path):
                print(f"ERROR: Script not found at {script_path}")
                print(f"Status: FAILED - File not found")
                messagebox.showerror("Error", f"Script not found:\n{script_path}")
                return

            # Run the script
            result = subprocess.run(
                ["python", script_path], capture_output=True, text=True, timeout=60
            )

            # Print output
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)

            if result.stderr:
                print("\nErrors:")
                print(result.stderr)

            # Check return code
            if result.returncode == 0:
                print(f"\nStatus: SUCCESS ✓")
                print(f"{script_name} executed successfully!")
                messagebox.showinfo("Success", f"{script_name} completed successfully!")
            else:
                print(f"\nStatus: FAILED ✗")
                print(f"Return code: {result.returncode}")
                messagebox.showerror(
                    "Failed",
                    f"{script_name} failed with return code {result.returncode}",
                )

        except subprocess.TimeoutExpired:
            print(f"\nStatus: FAILED ✗")
            print(f"Error: Script timed out (60 seconds)")
            messagebox.showerror("Timeout", f"{script_name} timed out after 60 seconds")

        except Exception as e:
            print(f"\nStatus: FAILED ✗")
            print(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to execute {script_name}:\n{str(e)}")

        print(f"{'=' * 50}\n")


def main():
    root = tk.Tk()
    app = ScriptLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
