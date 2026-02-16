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


class Theme:
    """Design system for consistent styling"""

    # Colors
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F8F9FA"
    BG_HOVER = "#E9ECEF"

    ACCENT_PRIMARY = "#4A90E2"
    ACCENT_HOVER = "#357ABD"
    ACCENT_DARK = "#2E5C8A"

    TEXT_PRIMARY = "#1A1A1A"
    TEXT_SECONDARY = "#6C757D"
    TEXT_LIGHT = "#ADB5BD"

    BORDER = "#DEE2E6"
    SUCCESS = "#28A745"
    ERROR = "#DC3545"
    WARNING = "#FFC107"

    # Fonts
    FONT_TITLE = ("Segoe UI", 24, "bold")
    FONT_SUBTITLE = ("Segoe UI", 12)
    FONT_CATEGORY = ("Segoe UI", 16, "bold")
    FONT_BUTTON = ("Segoe UI", 11)
    FONT_BUTTON_LARGE = ("Segoe UI", 13)
    FONT_STATUS = ("Segoe UI", 9)

    # Spacing
    PADDING_XL = 34
    PADDING_L = 18
    PADDING_M = 12
    PADDING_S = 6

    # Dimensions
    BUTTON_HEIGHT = 32
    BUTTON_HEIGHT_SMALL = 22
    BORDER_RADIUS = 6


class ModernButton(tk.Button):
    """Custom button with hover effects and modern styling"""

    def __init__(self, parent, style="primary", **kwargs):
        # Set default styling based on style type
        if style == "primary":
            defaults = {
                "bg": Theme.ACCENT_PRIMARY,
                "fg": "white",
                "activebackground": Theme.ACCENT_HOVER,
                "activeforeground": "white",
            }
            self.hover_color = Theme.ACCENT_HOVER
            self.normal_color = Theme.ACCENT_PRIMARY
        elif style == "secondary":
            defaults = {
                "bg": Theme.BG_SECONDARY,
                "fg": Theme.TEXT_PRIMARY,
                "activebackground": Theme.BG_HOVER,
                "activeforeground": Theme.TEXT_PRIMARY,
            }
            self.hover_color = Theme.BG_HOVER
            self.normal_color = Theme.BG_SECONDARY
        else:  # ghost/back button
            defaults = {
                "bg": Theme.BG_PRIMARY,
                "fg": Theme.TEXT_SECONDARY,
                "activebackground": Theme.BG_SECONDARY,
                "activeforeground": Theme.TEXT_PRIMARY,
            }
            self.hover_color = Theme.BG_SECONDARY
            self.normal_color = Theme.BG_PRIMARY

        defaults.update(
            {
                "font": kwargs.get("font", Theme.FONT_BUTTON),
                "relief": "flat",
                "cursor": "hand2",
                "bd": 0,
                "padx": 20,
                "pady": 12,
            }
        )

        # Merge with provided kwargs
        defaults.update(kwargs)

        super().__init__(parent, **defaults)

        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=self.hover_color)

    def _on_leave(self, e):
        self.config(bg=self.normal_color)


class ScriptLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Launcher")
        self.root.geometry("580x700")
        self.root.configure(bg=Theme.BG_PRIMARY)

        # Make window non-resizable for consistent layout
        self.root.resizable(False, False)

        load_dotenv()
        self.scripts = self.load_scripts()
        self.current_page = None

        # Main container with padding
        container = tk.Frame(root, bg=Theme.BG_PRIMARY)
        container.pack(fill="both", expand=True)

        # Content area
        self.main_frame = tk.Frame(container, bg=Theme.BG_PRIMARY)
        self.main_frame.pack(
            fill="both", expand=True, padx=Theme.PADDING_L, pady=Theme.PADDING_L
        )

        # Status bar at bottom
        self._create_status_bar(root)

        self.show_navigation()

    def _create_status_bar(self, root):
        """Create modern status bar"""
        status_frame = tk.Frame(root, bg=Theme.BG_SECONDARY, height=36)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor="w",
            bg=Theme.BG_SECONDARY,
            fg=Theme.TEXT_SECONDARY,
            font=Theme.FONT_STATUS,
            padx=Theme.PADDING_M,
        )
        self.status_label.pack(side="left", fill="both", expand=True)

        # Status indicator dot
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            bg=Theme.BG_SECONDARY,
            fg=Theme.SUCCESS,
            font=("Segoe UI", 12),
            padx=Theme.PADDING_M,
        )
        self.status_indicator.pack(side="right")

    def set_status(self, message: str, status_type: str = "ready"):
        """Update status bar with message and color indicator"""
        color_map = {
            "ready": Theme.SUCCESS,
            "running": Theme.WARNING,
            "error": Theme.ERROR,
            "success": Theme.SUCCESS,
        }

        self.root.after(0, lambda: self.status_var.set(message))
        self.root.after(
            0,
            lambda: self.status_indicator.config(
                fg=color_map.get(status_type, Theme.SUCCESS)
            ),
        )

    def load_scripts(self):
        try:
            scripts_json = os.getenv("SCRIPTS_LIST")
            if not scripts_json:
                return {}
            return json.loads(scripts_json)
        except Exception:
            return {}

    def show_navigation(self):
        """Display main navigation menu"""
        self.set_status("Ready", "ready")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Header section
        header_frame = tk.Frame(self.main_frame, bg=Theme.BG_PRIMARY)
        header_frame.pack(fill="x", pady=(0, Theme.PADDING_XL))

        title = tk.Label(
            header_frame,
            text="Script Launcher",
            font=Theme.FONT_TITLE,
            bg=Theme.BG_PRIMARY,
            fg=Theme.TEXT_PRIMARY,
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="Select a category to get started",
            font=Theme.FONT_SUBTITLE,
            bg=Theme.BG_PRIMARY,
            fg=Theme.TEXT_SECONDARY,
        )
        subtitle.pack(pady=(Theme.PADDING_S, 0))

        # Divider
        divider = tk.Frame(self.main_frame, bg=Theme.BORDER, height=1)
        divider.pack(fill="x", pady=Theme.PADDING_L)

        # Category buttons container
        button_container = tk.Frame(self.main_frame, bg=Theme.BG_PRIMARY)
        button_container.pack(fill="both", expand=True, pady=Theme.PADDING_M)

        categories = [
            ("💻 Coding", "coding"),
            ("💰 Finances", "finances"),
            ("☀️ Morning Activities", "morning"),
            ("📚 Study", "study"),
            ("📋 Planning", "planning"),
        ]

        for display_name, category_key in categories:
            btn = ModernButton(
                button_container,
                text=display_name,
                style="secondary",
                command=lambda cat=category_key, name=display_name: self.show_category(
                    cat, name
                ),
                font=Theme.FONT_BUTTON_LARGE,
                width=28,
                height=2,
            )
            btn.pack(pady=Theme.PADDING_S, ipady=4)

    def show_category(self, category, category_name):
        """Display scripts for selected category"""
        self.set_status(f"Viewing {category_name}", "ready")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Header with back button
        header_frame = tk.Frame(self.main_frame, bg=Theme.BG_PRIMARY)
        header_frame.pack(fill="x", pady=(0, Theme.PADDING_L))

        back_btn = ModernButton(
            header_frame,
            text="← Back",
            style="ghost",
            command=self.show_navigation,
            font=Theme.FONT_BUTTON,
        )
        back_btn.pack(side="left")

        # Clean category name (remove emoji for title)
        clean_name = (
            category_name.split(maxsplit=1)[-1]
            if " " in category_name
            else category_name
        )

        title = tk.Label(
            header_frame,
            text=clean_name,
            font=Theme.FONT_CATEGORY,
            bg=Theme.BG_PRIMARY,
            fg=Theme.TEXT_PRIMARY,
        )
        title.pack(side="left", padx=Theme.PADDING_M)

        # Divider
        divider = tk.Frame(self.main_frame, bg=Theme.BORDER, height=1)
        divider.pack(fill="x", pady=Theme.PADDING_M)

        # Scripts container with scrollbar if needed
        scripts_container = tk.Frame(self.main_frame, bg=Theme.BG_PRIMARY)
        scripts_container.pack(fill="both", expand=True, pady=Theme.PADDING_M)

        category_scripts = self.scripts.get(category, [])

        if not category_scripts:
            empty_state = tk.Label(
                scripts_container,
                text="No scripts available in this category",
                font=Theme.FONT_SUBTITLE,
                bg=Theme.BG_PRIMARY,
                fg=Theme.TEXT_LIGHT,
            )
            empty_state.pack(pady=Theme.PADDING_XL)
            return

        # Script buttons
        for script in category_scripts:
            script_name = script.get("name", "Unnamed Script")
            module_path = script.get("module", "")

            # Script card frame
            card_frame = tk.Frame(scripts_container, bg=Theme.BG_SECONDARY)
            card_frame.pack(fill="x", pady=Theme.PADDING_S)

            btn = ModernButton(
                card_frame,
                text=script_name,
                style="secondary",
                command=lambda n=script_name, m=module_path: self.run_script(n, m),
                font=Theme.FONT_BUTTON,
                width=50,
                anchor="w",
            )
            btn.pack(fill="x", padx=2, pady=2, ipady=8)

    def run_script(self, script_name: str, module_path: str):
        """Execute script in background thread"""
        self.set_status(f"Launching {script_name}...", "running")
        threading.Thread(
            target=self._run_script_worker,
            args=(script_name, module_path),
            daemon=True,
        ).start()

    def _run_script_worker(self, script_name: str, module_path: str):
        """Background worker for script execution"""
        try:
            self.set_status(f"Running {script_name}...", "running")

            subprocess.run(
                [sys.executable, "-m", module_path],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )

            self.set_status(f"✓ {script_name} completed", "success")

            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", f"{script_name} completed successfully!"
                ),
            )

        except subprocess.TimeoutExpired:
            self.set_status(f"✗ {script_name} timed out", "error")
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Timeout", f"{script_name} exceeded 60 seconds"
                ),
            )

        except subprocess.CalledProcessError:
            self.set_status(f"✗ {script_name} failed", "error")
            self.root.after(
                0,
                lambda: messagebox.showerror("Failed", f"{script_name} failed"),
            )

        except Exception as e:
            self.set_status(f"✗ Error in {script_name}", "error")
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
