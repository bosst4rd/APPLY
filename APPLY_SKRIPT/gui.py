"""
APPLY - Configuration Migration Tool
eXpletus Design mit CustomTkinter
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Any
from collect_parser import CollectParser
from config_applier import ConfigApplier
from expletus_style import *


class ApplyGUI(ctk.CTk):
    """APPLY GUI mit eXpletus Design"""

    def __init__(self):
        super().__init__()

        # Theme initialisieren
        init_theme()

        # Window konfigurieren
        self.title("eXpletus APPLY")
        self.geometry("800x600")
        self.resizable(False, False)

        # Data
        self.parser = None
        self.applier = None
        self.selected_configs = {}
        self.checkboxes = {}
        self.is_running = False

        # Create GUI
        self.create_gui()

    def create_gui(self):
        """Erstelle GUI-Elemente"""

        # Header mit Logo
        create_header(self, "eXpletus APPLY", "v2.2")

        # Main content area
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 1. File selection
        file_frame = ctk.CTkFrame(content)
        file_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(file_frame, text="COLLECT Datei:", font=Fonts.SUBTITLE).pack(anchor="w", padx=10, pady=(10, 5))

        file_inner = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_inner.pack(fill="x", padx=10, pady=(0, 10))

        self.file_entry = ctk.CTkEntry(file_inner, height=Sizes.ENTRY_HEIGHT, placeholder_text="Bitte JSON-Datei auswählen...")
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.browse_btn = ctk.CTkButton(file_inner, text="Durchsuchen", command=self.browse_file,
                                        height=Sizes.BUTTON_SMALL, width=100, font=Fonts.BUTTON)
        self.browse_btn.pack(side="left", padx=(0, 5))

        self.load_btn = ctk.CTkButton(file_inner, text="Laden", command=self.load_file,
                                      height=Sizes.BUTTON_SMALL, width=80, font=Fonts.BUTTON,
                                      fg_color=Colors.GREEN, hover_color=Colors.GREEN_HOVER)
        self.load_btn.pack(side="left")

        # 2. Configuration selection (scrollable)
        config_frame = ctk.CTkFrame(content)
        config_frame.pack(fill="both", expand=True, pady=(0, 10))

        ctk.CTkLabel(config_frame, text="Konfigurationen auswählen:", font=Fonts.SUBTITLE).pack(anchor="w", padx=10, pady=(10, 5))

        # Scrollable frame for checkboxes
        self.scroll_frame = ctk.CTkScrollableFrame(config_frame, height=250)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Button row for select all/none
        btn_row = ctk.CTkFrame(config_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(btn_row, text="Alle auswählen", command=self.select_all,
                     height=Sizes.BUTTON_SMALL, font=Fonts.SMALL, width=100).pack(side="left", padx=(0, 5))
        ctk.CTkButton(btn_row, text="Alle abwählen", command=self.deselect_all,
                     height=Sizes.BUTTON_SMALL, font=Fonts.SMALL, width=100).pack(side="left")

        # 3. Options
        options_frame = ctk.CTkFrame(content)
        options_frame.pack(fill="x", pady=(0, 10))

        opt_inner = ctk.CTkFrame(options_frame, fg_color="transparent")
        opt_inner.pack(fill="x", padx=10, pady=10)

        self.dry_run_var = ctk.BooleanVar(value=True)
        self.dry_run_check = ctk.CTkCheckBox(opt_inner, text="Dry Run (nur simulieren, nichts ändern)",
                                             variable=self.dry_run_var, font=Fonts.NORMAL)
        self.dry_run_check.pack(side="left")

        self.backup_var = ctk.BooleanVar(value=True)
        self.backup_check = ctk.CTkCheckBox(opt_inner, text="Backup vor Änderungen erstellen",
                                            variable=self.backup_var, font=Fonts.NORMAL)
        self.backup_check.pack(side="left", padx=(20, 0))

        # 4. Progress bar
        self.progress_bar = create_progress_bar(content, width=780)
        self.progress_bar.pack(fill="x", pady=(0, 5))

        self.status_label = ctk.CTkLabel(content, text="Bereit", font=Fonts.STATUS, text_color=Colors.MUTED)
        self.status_label.pack(fill="x", pady=(0, 10))

        # 5. Log output
        self.log_box = create_log_textbox(content, height=100)
        self.log_box.pack(fill="both", expand=True)
        self.log_box.configure(state="disabled")

        # Bottom button row
        btn_frame = create_button_row(self)

        self.start_btn = create_start_button(btn_frame, self.start_apply, "▶ ANWENDEN")
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.start_btn.configure(state="disabled")

        self.stop_btn = create_stop_button(btn_frame, self.stop_apply)
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # MoBackup button (hidden by default)
        self.mobackup_btn = ctk.CTkButton(btn_frame, text="📧 MoBackup starten",
                                          command=self.start_mobackup,
                                          height=Sizes.BUTTON_HEIGHT, font=Fonts.BUTTON,
                                          fg_color="#ff8800", hover_color="#dd7700")
        self.mobackup_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.mobackup_btn.pack_forget()  # Hide initially

        exit_btn = create_exit_button(btn_frame, self.quit_app)
        exit_btn.pack(side="right")

    def browse_file(self):
        """Datei-Browser öffnen"""
        filename = filedialog.askopenfilename(
            title="COLLECT Datei auswählen",
            filetypes=(("JSON Dateien", "*.json"), ("Alle Dateien", "*.*"))
        )
        if filename:
            self.file_entry.delete(0, "end")
            self.file_entry.insert(0, filename)

    def load_file(self):
        """COLLECT Datei laden"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine Datei aus")
            return

        self.log("Lade Datei: " + file_path)

        try:
            self.parser = CollectParser(file_path)
            if self.parser.load():
                self.log("✓ Datei erfolgreich geladen")

                # Check if configurations exist
                categories = self.parser.get_categories()
                if not categories:
                    self.log("⚠️ Warnung: Keine Konfigurationen in der Datei gefunden")
                    messagebox.showwarning("Warnung", "Die JSON-Datei enthält keine Konfigurationen.\n\nErwartet wird eine 'configurations' Struktur.")
                    return

                self.populate_configs()
                self.start_btn.configure(state="normal")
            else:
                messagebox.showerror("Fehler", "Fehler beim Laden der Datei")
                self.log("✗ Fehler beim Laden der Datei")
        except json.JSONDecodeError as e:
            error_msg = f"Ungültige JSON-Datei:\n{str(e)}"
            messagebox.showerror("JSON-Fehler", error_msg)
            self.log(f"✗ JSON-Fehler: {str(e)}")
        except Exception as e:
            error_msg = f"Fehler beim Laden:\n{str(e)}"
            messagebox.showerror("Fehler", error_msg)
            self.log(f"✗ Fehler: {str(e)}")
            import traceback
            self.log(traceback.format_exc())

    def populate_configs(self):
        """Konfigurationen in der Liste anzeigen"""
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.checkboxes = {}
        self.selected_configs = {}

        if not self.parser:
            return

        # System info (read-only)
        system_info = self.parser.get_system_info()
        if system_info:
            info_label = ctk.CTkLabel(self.scroll_frame, text="📋 System-Information:",
                                     font=Fonts.SUBTITLE, anchor="w")
            info_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(5, 5))

            row = 1
            for key, value in system_info.items():
                label = ctk.CTkLabel(self.scroll_frame, text=f"  • {key}: {value}",
                                    font=Fonts.SMALL, text_color=Colors.MUTED, anchor="w")
                label.grid(row=row, column=0, columnspan=2, sticky="w", padx=(20, 0))
                row += 1

            # Separator
            sep = ctk.CTkFrame(self.scroll_frame, height=2, fg_color=Colors.GRAY)
            sep.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
            row += 1
        else:
            row = 0

        # Categories mit Checkboxes
        categories = self.parser.get_categories()

        category_info = {
            'hostname': ('🖥️', 'Hostname'),
            'username': ('👤', 'Benutzername'),
            'domain': ('🏢', 'Domäne'),
            'workgroup': ('👥', 'Arbeitsgruppe'),
            'network': ('🌐', 'Netzwerk'),
            'ipv4_network': ('🌐', 'IPv4-Netzwerk'),
            'routes': ('🛣️', 'Ständige Routen'),
            'ipv4_routes': ('🛣️', 'Ständige Routen IPv4'),
            'network_drives': ('💾', 'Netzlaufwerke'),
            'netzlaufwerke': ('💾', 'Netzlaufwerke'),
            'default_browser': ('🌍', 'Standard-Browser'),
            'default_pdf': ('📄', 'Standard-PDF-Anwendung'),
            'default_mail': ('📧', 'Standard-Mailprogramm'),
            'default_word': ('📝', 'Standard für Word-Dokumente'),
            'default_apps': ('⚙️', 'Standard-Anwendungen'),
            'browser_favorites': ('⭐', 'Browser-Favoriten'),
            'browser_favoriten': ('⭐', 'Browser-Favoriten'),
            'mobackup': ('💼', 'MoBackup (Outlook-Backup)')
        }

        for category in categories:
            icon, display_name = category_info.get(category, ('•', category.capitalize()))

            # Category header
            header = ctk.CTkLabel(self.scroll_frame, text=f"{icon} {display_name}:",
                                 font=Fonts.SUBTITLE, anchor="w")
            header.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
            row += 1

            items = self.parser.get_category_items(category)

            if isinstance(items, dict):
                for item_key, item_value in items.items():
                    var = ctk.BooleanVar(value=True)
                    config_key = f"{category}.{item_key}"
                    self.checkboxes[config_key] = var
                    self.selected_configs[config_key] = var

                    # Description
                    if isinstance(item_value, dict):
                        desc = item_value.get('description', '')
                    else:
                        desc = str(item_value)[:60]

                    # Checkbox
                    cb = ctk.CTkCheckBox(self.scroll_frame, text=f"{item_key}",
                                        variable=var, font=Fonts.NORMAL)
                    cb.grid(row=row, column=0, sticky="w", padx=(20, 10))

                    # Description label
                    desc_label = ctk.CTkLabel(self.scroll_frame, text=desc,
                                             font=Fonts.SMALL, text_color=Colors.MUTED, anchor="w")
                    desc_label.grid(row=row, column=1, sticky="w")
                    row += 1

            elif isinstance(items, str):
                var = ctk.BooleanVar(value=True)
                config_key = f"{category}.value"
                self.checkboxes[config_key] = var
                self.selected_configs[config_key] = var

                cb = ctk.CTkCheckBox(self.scroll_frame, text=f"Wiederherstellen: {items}",
                                    variable=var, font=Fonts.NORMAL)
                cb.grid(row=row, column=0, columnspan=2, sticky="w", padx=(20, 10))
                row += 1

        self.log(f"✓ {len(categories)} Kategorien mit {len(self.checkboxes)} Elementen geladen")

        # Check if MoBackup category exists
        if 'mobackup' in categories or any('outlook' in cat.lower() for cat in categories):
            self.mobackup_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
            self.log("💼 MoBackup verfügbar - Button aktiviert")

    def select_all(self):
        """Alle auswählen"""
        for var in self.checkboxes.values():
            var.set(True)
        self.log("✓ Alle Konfigurationen ausgewählt")

    def deselect_all(self):
        """Alle abwählen"""
        for var in self.checkboxes.values():
            var.set(False)
        self.log("○ Alle Konfigurationen abgewählt")

    def start_apply(self):
        """Konfigurationen anwenden"""
        if not self.parser:
            messagebox.showerror("Fehler", "Keine Daten geladen")
            return

        dry_run = self.dry_run_var.get()
        mode = "Dry Run (Simulation)" if dry_run else "ECHTE ÄNDERUNGEN"

        if not dry_run:
            response = messagebox.askyesno(
                "Bestätigung",
                "⚠️ WARNUNG: Dies wird echte Änderungen am System vornehmen!\n\n"
                "Möchten Sie fortfahren?"
            )
            if not response:
                return

        self.log(f"\n{'='*60}")
        self.log(f"Starte Migration im Modus: {mode}")
        self.log(f"{'='*60}\n")

        # UI anpassen
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="Migration läuft...", text_color=Colors.SUCCESS)

        # Thread starten
        thread = threading.Thread(target=self._apply_thread, args=(dry_run,))
        thread.daemon = True
        thread.start()

    def _apply_thread(self, dry_run: bool):
        """Apply-Thread"""
        try:
            self.applier = ConfigApplier(dry_run=dry_run, create_backup=self.backup_var.get())
            categories = self.parser.get_categories()

            # Count selected items
            selected_count = sum(1 for key, var in self.checkboxes.items() if var.get())
            processed = 0

            for category in categories:
                if not self.is_running:
                    self.log("\n⚠️ Migration abgebrochen")
                    break

                items = self.parser.get_category_items(category)
                if not isinstance(items, dict):
                    continue

                for item_key, item_value in items.items():
                    if not self.is_running:
                        break

                    config_key = f"{category}.{item_key}"

                    if config_key in self.checkboxes and self.checkboxes[config_key].get():
                        self.log(f"Anwenden: {category} -> {item_key}")
                        self.status_label.configure(text=f"Verarbeite: {category} -> {item_key}")

                        success, message = self.applier.apply_configuration(category, item_value)

                        if success:
                            self.log(f"  ✓ {message}")
                        else:
                            self.log(f"  ✗ {message}")

                        processed += 1
                        progress = processed / selected_count if selected_count > 0 else 0
                        self.progress_bar.set(progress)

            # Summary
            summary = self.applier.get_summary()
            self.log(f"\n{'='*60}")
            self.log(f"Migration abgeschlossen!")
            self.log(f"{'='*60}")
            self.log(f"Erfolgreich: {summary['applied_count']}")
            self.log(f"Fehler: {summary['error_count']}")

            if summary['errors']:
                self.log("\nFehler:")
                for error in summary['errors']:
                    self.log(f"  - {error}")

            self.status_label.configure(text="Abgeschlossen", text_color=Colors.SUCCESS)

            messagebox.showinfo(
                "Abgeschlossen",
                f"Migration abgeschlossen!\n\n"
                f"Erfolgreich: {summary['applied_count']}\n"
                f"Fehler: {summary['error_count']}"
            )

        except Exception as e:
            self.log(f"\n✗ FEHLER: {str(e)}")
            self.status_label.configure(text="Fehler aufgetreten", text_color=Colors.ERROR)
            messagebox.showerror("Fehler", f"Fehler bei der Migration: {str(e)}")

        finally:
            self.is_running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def stop_apply(self):
        """Migration stoppen"""
        self.is_running = False
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Wird gestoppt...", text_color=Colors.ERROR)
        self.log("\n⚠️ Stopp angefordert...")

    def log(self, message: str):
        """Log-Nachricht hinzufügen"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_idletasks()

    def start_mobackup(self):
        """MoBackup starten"""
        mobackup_path = Path("assets/Mobackup/mobackup.exe")

        if not mobackup_path.exists():
            messagebox.showerror("Fehler", f"MoBackup nicht gefunden:\n{mobackup_path.absolute()}")
            self.log(f"✗ MoBackup nicht gefunden: {mobackup_path}")
            return

        try:
            self.log("🚀 Starte MoBackup...")
            if platform.system() == 'Windows':
                subprocess.Popen([str(mobackup_path)], shell=True)
                self.log("✓ MoBackup gestartet")
                messagebox.showinfo("MoBackup", "MoBackup wurde gestartet.\n\nBitte konfigurieren Sie Ihr Outlook-Backup dort.")
            else:
                messagebox.showwarning("Nicht unterstützt", "MoBackup ist nur unter Windows verfügbar")
                self.log("⚠️ MoBackup nur unter Windows verfügbar")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Starten von MoBackup:\n{str(e)}")
            self.log(f"✗ Fehler beim Starten von MoBackup: {str(e)}")

    def quit_app(self):
        """App beenden"""
        if self.is_running:
            response = messagebox.askyesno("Beenden?", "Migration läuft noch. Wirklich beenden?")
            if not response:
                return
            self.is_running = False
        self.quit()


def main():
    """Main entry point"""
    app = ApplyGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
