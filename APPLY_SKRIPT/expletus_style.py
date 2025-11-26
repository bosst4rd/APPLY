#!/usr/bin/env python3
"""
eXpletus Style-Konfiguration
Gemeinsame Optik für alle eXpletus-Tools (COLLECT, APPLY, etc.)
"""

import customtkinter as ctk
from pathlib import Path
from PIL import Image

# === THEME INITIALISIEREN ===
def init_theme():
    """Theme initialisieren - am Anfang jeder App aufrufen"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


# === FARBEN ===
class Colors:
    # Buttons
    GREEN = "#28a745"
    GREEN_HOVER = "#218838"
    RED = "#dc3545"
    RED_HOVER = "#c82333"
    GRAY = "#555"
    GRAY_HOVER = "#444"

    # Text
    SUCCESS = "#8f8"      # Grün für ✓
    ERROR = "#f88"        # Rot für ✗
    MUTED = "gray"        # Hinweistexte

    # Hintergrund
    TRANSPARENT = "transparent"


# === SCHRIFTEN ===
class Fonts:
    TITLE = ("Arial", 16, "bold")
    SUBTITLE = ("Arial", 11, "bold")
    NORMAL = ("Arial", 10)
    SMALL = ("Arial", 9)
    BUTTON_LARGE = ("Arial", 13, "bold")
    BUTTON = ("Arial", 11)
    LOG = ("Consolas", 9)
    STATUS = ("Consolas", 10)


# === GRÖSSEN ===
class Sizes:
    WINDOW = "680x480"
    BUTTON_HEIGHT = 40
    BUTTON_SMALL = 28
    ENTRY_HEIGHT = 26
    LOGO_HEIGHT = 36
    PROGRESS_HEIGHT = 14


# === ANIMATION ===
class Animation:
    SPINNER = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    DOTS = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


# === HELPER FUNKTIONEN ===

def get_logo_path():
    """Gibt den Pfad zum Logo zurück"""
    # Versuche verschiedene Pfade
    possible_paths = [
        Path(__file__).parent.parent / "media" / "expletus_1.png",
        Path(__file__).parent / "media" / "expletus_1.png",
        Path("media") / "expletus_1.png",
    ]
    for p in possible_paths:
        if p.exists():
            return p
    return None


def load_logo(height=36):
    """Lädt das Logo mit korrektem Seitenverhältnis"""
    logo_path = get_logo_path()
    if logo_path and logo_path.exists():
        img = Image.open(logo_path)
        w = int(img.width * (height / img.height))
        img = img.resize((w, height), Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, height))
    return None


def create_header(parent, title, version, show_logo=True):
    """Erstellt einen Standard-Header mit Logo und Titel"""
    header = ctk.CTkFrame(parent, fg_color=Colors.TRANSPARENT, height=50)
    header.pack(fill="x", padx=10, pady=(8, 0))
    header.pack_propagate(False)

    # Logo
    if show_logo:
        logo = load_logo(Sizes.LOGO_HEIGHT)
        if logo:
            ctk.CTkLabel(header, image=logo, text="").pack(side="left")
            # Logo-Referenz speichern um Garbage Collection zu verhindern
            header._logo = logo

    # Titel
    title_box = ctk.CTkFrame(header, fg_color=Colors.TRANSPARENT)
    title_box.pack(side="left", padx=10)
    ctk.CTkLabel(title_box, text=title, font=Fonts.TITLE).pack(anchor="w")
    ctk.CTkLabel(title_box, text=version, font=Fonts.SMALL, text_color=Colors.MUTED).pack(anchor="w")

    return header


def create_button_row(parent):
    """Erstellt eine Standard-Button-Zeile am unteren Rand"""
    btn_frame = ctk.CTkFrame(parent, fg_color=Colors.TRANSPARENT)
    btn_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 10))
    return btn_frame


def create_start_button(parent, command, text="▶ STARTEN"):
    """Erstellt einen grünen Start-Button"""
    return ctk.CTkButton(
        parent, text=text, command=command,
        height=Sizes.BUTTON_HEIGHT, font=Fonts.BUTTON_LARGE,
        fg_color=Colors.GREEN, hover_color=Colors.GREEN_HOVER
    )


def create_stop_button(parent, command, text="■ STOPP"):
    """Erstellt einen roten Stopp-Button"""
    return ctk.CTkButton(
        parent, text=text, command=command,
        height=Sizes.BUTTON_HEIGHT, font=Fonts.BUTTON_LARGE,
        fg_color=Colors.RED, hover_color=Colors.RED_HOVER,
        state="disabled"
    )


def create_exit_button(parent, command, text="Beenden"):
    """Erstellt einen grauen Beenden-Button"""
    return ctk.CTkButton(
        parent, text=text, command=command,
        height=Sizes.BUTTON_HEIGHT, font=Fonts.BUTTON,
        fg_color=Colors.GRAY, hover_color=Colors.GRAY_HOVER,
        width=90
    )


def create_progress_bar(parent, width=200):
    """Erstellt eine Standard-Progressbar"""
    bar = ctk.CTkProgressBar(parent, width=width, height=Sizes.PROGRESS_HEIGHT)
    bar.set(0)
    return bar


def create_log_textbox(parent, height=100):
    """Erstellt eine Standard-Log-Textbox"""
    return ctk.CTkTextbox(parent, height=height, font=Fonts.LOG)


def format_progress(message, progress, anim_idx=0):
    """Formatiert Progress-Anzeige im winget-Style"""
    char = Animation.SPINNER[anim_idx % len(Animation.SPINNER)]
    pct = int(progress * 100)
    bar_len = 20
    filled = int(bar_len * progress)
    bar = "█" * filled + "░" * (bar_len - filled)
    return f"{char} [{bar}] {pct}% {message}"


# === BEISPIEL-VERWENDUNG ===
"""
from expletus_style import *

# Am Anfang der App:
init_theme()

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(Sizes.WINDOW)
        self.resizable(False, False)

        # Header
        create_header(self, "eXpletus APPLY", "v1.0")

        # Buttons
        btn_frame = create_button_row(self)
        start = create_start_button(btn_frame, self.start)
        start.pack(side="left", fill="x", expand=True, padx=(0, 5))
"""
