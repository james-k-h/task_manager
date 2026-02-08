import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from dotenv import load_dotenv
import json
import sys
from pathlib import Path
import threading

BASE_DIR = Path(__file__).resolve().parent


class ScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Launcher")
        self.root.geometry("600x600")
        self.root.configure(bg="white")

        load_dotenv()
        self.scripts = self.load_scripts()
        self.current_page = None

        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(
            root,
            textvariable=self.status_var,
            anchor="w",
            bg="#eeeeee",
            fg="#333333",
            padx=10,
        )
        self.status_bar.pack(side="bottom", fill="x")

        self.show_navigation()

    def set_status(self, message: str):
        self.root.after(0, lambda: self.status_var.set(message))

    def load_scripts(self):
        try:
            scripts_json = os.getenv("SCRIPTS_LIST")
            if not scripts_json:
                return {}
            return json.loads(scripts_json)
        except Exception:
            return {}

    def show_navigation(self):
        self.set_status("Ready")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.main_frame,
            text="Script Launcher",
            font=("Arial", 14, "bold"),
            bg="white",
        )
        title.pack(pady=14)

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(pady=12, padx=30, fill="both", expand=True)

        categories = [
            ("Coding", "coding"),
            ("Finances", "finances"),
            ("Morning Activities", "morning"),
            ("Study", "study"),
            ("Planning", "planning"),
        ]

        for display_name, category_key in categories:
            tk.Button(
                button_frame,
                text=display_name,
                command=lambda cat=category_key, name=display_name: self.show_category(
                    cat, name
                ),
                bg="#d3d3d3",
                font=("Arial", 14),
                width=20,
                height=2,
            ).pack(pady=15)

    def show_category(self, category, category_name):
        self.set_status("Ready")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header_frame = tk.Frame(self.main_frame, bg="white")
        header_frame.pack(fill="x", pady=20, padx=20)

        tk.Button(
            header_frame,
            text="← Back",
            command=self.show_navigation,
            bg="#e0e0e0",
            relief="flat",
        ).pack(side="left")

        tk.Label(
            header_frame,
            text=category_name,
            font=("Arial", 18, "bold"),
            bg="white",
        ).pack(side="left", padx=20)

        scripts_frame = tk.Frame(self.main_frame, bg="white")
        scripts_frame.pack(pady=10, padx=40, fill="both", expand=True)

        category_scripts = self.scripts.get(category, [])

        for script in category_scripts:
            script_name = script.get("name")
            module_path = script.get("module")

            tk.Button(
                scripts_frame,
                text=script_name,
                command=lambda n=script_name, m=module_path: self.run_script(n, m),
                bg="#d3d3d3",
                font=("Arial", 11),
                width=35,
                height=2,
            ).pack(pady=8)

    def run_script(self, script_name: str, module_path: str):
        self.set_status(f"Launching {script_name}...")
        threading.Thread(
            target=self._run_script_worker,
            args=(script_name, module_path),
            daemon=True,
        ).start()

    def _run_script_worker(self, script_name: str, module_path: str):
        try:
            self.set_status("Starting script...")

            subprocess.run(
                [sys.executable, "-m", module_path],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            self.set_status("Done")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", f"{script_name} completed successfully!"
                ),
            )

        except subprocess.TimeoutExpired:
            self.set_status("Timed out")
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Timeout", f"{script_name} exceeded 60 seconds"
                ),
            )

        except subprocess.CalledProcessError:
            self.set_status("Failed")
            self.root.after(
                0,
                lambda: messagebox.showerror("Failed", f"{script_name} failed"),
            )

        except Exception as e:
            self.set_status("Error")
            self.root.after(
                0,
                lambda: messagebox.showerror("Error", f"{script_name} error:\n{e}"),
            )


def main():
    root = tk.Tk()
    ScriptLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
