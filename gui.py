"""
COLLECT Configuration Migration Tool - GUI
Enhanced with checkbox selection and ALBIS-Registry support
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from typing import Dict, List, Any
from collect_parser import CollectParser
from config_applier import ConfigApplier


class MigrationToolGUI:
    """Main GUI application for the migration tool"""

    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("APPLY - Configuration Migration Tool")
        self.root.geometry("1000x750")

        # Data
        self.parser = None
        self.applier = None
        self.selected_configs = {}
        self.checkboxes = {}  # Store checkbox variables

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="APPLY - Configuration Migration Tool",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="1. COLLECT Datei auswählen", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60)
        file_entry.grid(row=0, column=0, padx=(0, 10))

        browse_btn = ttk.Button(file_frame, text="Durchsuchen...", command=self.browse_file)
        browse_btn.grid(row=0, column=1, padx=(0, 10))

        load_btn = ttk.Button(file_frame, text="Laden", command=self.load_file)
        load_btn.grid(row=0, column=2)

        # Configuration selection frame with canvas for scrolling
        config_frame = ttk.LabelFrame(
            main_frame,
            text="2. Konfigurationen zum Wiederherstellen auswählen",
            padding="10"
        )
        config_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(0, weight=1)

        # Canvas with scrollbar for checkboxes
        canvas_frame = ttk.Frame(config_frame)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, height=300)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Buttons for selection
        btn_frame = ttk.Frame(config_frame)
        btn_frame.grid(row=1, column=0, pady=(10, 0))

        select_all_btn = ttk.Button(btn_frame, text="Alle auswählen", command=self.select_all)
        select_all_btn.grid(row=0, column=0, padx=5)

        deselect_all_btn = ttk.Button(btn_frame, text="Alle abwählen", command=self.deselect_all)
        deselect_all_btn.grid(row=0, column=1, padx=5)

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="3. Optionen", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.dry_run_var = tk.BooleanVar(value=True)
        dry_run_check = ttk.Checkbutton(
            options_frame,
            text="Dry Run (nur simulieren, nichts ändern)",
            variable=self.dry_run_var
        )
        dry_run_check.grid(row=0, column=0)

        # Apply button
        apply_frame = ttk.Frame(main_frame)
        apply_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        self.apply_btn = ttk.Button(
            apply_frame,
            text="Konfigurationen anwenden",
            command=self.apply_configurations,
            state="disabled"
        )
        self.apply_btn.grid(row=0, column=0)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(6, weight=1)

    def browse_file(self):
        """Open file browser to select COLLECT file"""
        filename = filedialog.askopenfilename(
            title="COLLECT Datei auswählen",
            filetypes=(("JSON Dateien", "*.json"), ("Alle Dateien", "*.*"))
        )
        if filename:
            self.file_path_var.set(filename)

    def load_file(self):
        """Load and parse the selected COLLECT file"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine Datei aus")
            return

        self.log("Lade Datei: " + file_path)

        try:
            self.parser = CollectParser(file_path)
            if self.parser.load():
                self.log("Datei erfolgreich geladen")
                self.populate_tree()
                self.apply_btn.config(state="normal")
            else:
                messagebox.showerror("Fehler", "Fehler beim Laden der Datei")
                self.log("Fehler beim Laden der Datei")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei: {str(e)}")
            self.log(f"Fehler: {str(e)}")

    def populate_tree(self):
        """Populate the scrollable frame with checkboxes for configurations"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.checkboxes = {}
        self.selected_configs = {}

        if not self.parser:
            return

        row = 0

        # Add system info (read-only, no checkbox)
        system_info = self.parser.get_system_info()
        if system_info:
            info_label = ttk.Label(
                self.scrollable_frame,
                text="📋 System-Information (von Quelle):",
                font=("Arial", 11, "bold"),
                foreground="blue"
            )
            info_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(5, 5))
            row += 1

            for key, value in system_info.items():
                info_text = ttk.Label(
                    self.scrollable_frame,
                    text=f"  • {key}: {value}",
                    foreground="gray"
                )
                info_text.grid(row=row, column=0, columnspan=3, sticky=tk.W, padx=(20, 0))
                row += 1

            # Separator
            ttk.Separator(self.scrollable_frame, orient='horizontal').grid(
                row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10
            )
            row += 1

        # Add configurations with checkboxes
        categories = self.parser.get_categories()

        # Define category display order and icons
        category_info = {
            'hostname': ('🖥️', 'Hostname'),
            'network': ('🌐', 'Netzwerk'),
            'albis_registry': ('📝', 'ALBIS-Registry'),
            'users': ('👤', 'Benutzernamen'),
            'packages': ('📦', 'Installierte Software'),
            'services': ('⚙️', 'Dienste'),
            'files': ('📁', 'Dateien')
        }

        for category in categories:
            icon, display_name = category_info.get(category, ('•', category.capitalize()))

            # Category header
            category_label = ttk.Label(
                self.scrollable_frame,
                text=f"{icon} {display_name}:",
                font=("Arial", 10, "bold")
            )
            category_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
            row += 1

            items = self.parser.get_category_items(category)

            # Handle different data structures
            if isinstance(items, dict):
                for item_key, item_value in items.items():
                    var = tk.BooleanVar(value=True)
                    config_key = f"{category}.{item_key}"
                    self.checkboxes[config_key] = var
                    self.selected_configs[config_key] = var

                    # Get description
                    if isinstance(item_value, dict):
                        desc = item_value.get('description', '')
                        # For packages, show if installable
                        if category == 'packages':
                            pkg_list = item_value.get('packages', [])
                            if isinstance(pkg_list, list):
                                desc = f"{len(pkg_list)} Pakete"
                    else:
                        desc = str(item_value)[:60]

                    # Checkbox
                    cb = ttk.Checkbutton(
                        self.scrollable_frame,
                        text=f"{item_key}",
                        variable=var
                    )
                    cb.grid(row=row, column=0, sticky=tk.W, padx=(20, 10))

                    # Description
                    desc_label = ttk.Label(
                        self.scrollable_frame,
                        text=desc,
                        foreground="gray"
                    )
                    desc_label.grid(row=row, column=1, sticky=tk.W, padx=(0, 10))

                    # Action label for packages
                    if category == 'packages' and isinstance(item_value, dict):
                        action_label = ttk.Label(
                            self.scrollable_frame,
                            text="→ zur Installation vormerken",
                            foreground="green",
                            font=("Arial", 8)
                        )
                        action_label.grid(row=row, column=2, sticky=tk.W)

                    row += 1
            elif isinstance(items, str):
                # Single value like hostname
                var = tk.BooleanVar(value=True)
                config_key = f"{category}.value"
                self.checkboxes[config_key] = var
                self.selected_configs[config_key] = var

                cb = ttk.Checkbutton(
                    self.scrollable_frame,
                    text=f"Wiederherstellen: {items}",
                    variable=var
                )
                cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=(20, 10))
                row += 1

        self.log(f"✓ {len(categories)} Kategorien mit {len(self.checkboxes)} Elementen geladen")

    def select_all(self):
        """Select all configurations"""
        for var in self.checkboxes.values():
            var.set(True)
        self.log("✓ Alle Konfigurationen ausgewählt")

    def deselect_all(self):
        """Deselect all configurations"""
        for var in self.checkboxes.values():
            var.set(False)
        self.log("○ Alle Konfigurationen abgewählt")

    def apply_configurations(self):
        """Apply selected configurations"""
        if not self.parser:
            messagebox.showerror("Fehler", "Keine Daten geladen")
            return

        # Confirm action
        dry_run = self.dry_run_var.get()
        mode = "Dry Run (Simulation)" if dry_run else "ECHTE ÄNDERUNGEN"

        if not dry_run:
            response = messagebox.askyesno(
                "Bestätigung",
                "WARNUNG: Dies wird echte Änderungen am System vornehmen!\n\n"
                "Möchten Sie fortfahren?"
            )
            if not response:
                return

        self.log(f"\n{'='*60}")
        self.log(f"Starte Migration im Modus: {mode}")
        self.log(f"{'='*60}\n")

        # Disable apply button during operation
        self.apply_btn.config(state="disabled")
        self.progress_var.set(0)

        # Run in thread to keep GUI responsive
        thread = threading.Thread(target=self._apply_configurations_thread, args=(dry_run,))
        thread.start()

    def _apply_configurations_thread(self, dry_run: bool):
        """Apply configurations in a separate thread"""
        try:
            self.applier = ConfigApplier(dry_run=dry_run)
            categories = self.parser.get_categories()
            total_items = sum(len(self.parser.get_category_items(cat)) for cat in categories)
            processed = 0

            for category in categories:
                items = self.parser.get_category_items(category)
                if not isinstance(items, dict):
                    continue

                for item_key, item_value in items.items():
                    config_key = f"{category}.{item_key}"

                    # Check if checkbox is selected
                    if config_key in self.checkboxes and self.checkboxes[config_key].get():
                        self.log(f"Anwenden: {category} -> {item_key}")

                        success, message = self.applier.apply_configuration(category, item_value)

                        if success:
                            self.log(f"  ✓ {message}")
                        else:
                            self.log(f"  ✗ {message}")

                    processed += 1
                    progress = (processed / total_items) * 100
                    self.progress_var.set(progress)

            # Show summary
            summary = self.applier.get_summary()
            self.log(f"\n{'='*60}")
            self.log(f"Migration abgeschlossen!")
            self.log(f"{'='*60}")
            self.log(f"Erfolgreich angewendet: {summary['applied_count']}")
            self.log(f"Fehler: {summary['error_count']}")

            if summary['errors']:
                self.log("\nFehler:")
                for error in summary['errors']:
                    self.log(f"  - {error}")

            messagebox.showinfo(
                "Abgeschlossen",
                f"Migration abgeschlossen!\n\n"
                f"Erfolgreich: {summary['applied_count']}\n"
                f"Fehler: {summary['error_count']}"
            )

        except Exception as e:
            self.log(f"FEHLER: {str(e)}")
            messagebox.showerror("Fehler", f"Fehler bei der Migration: {str(e)}")

        finally:
            self.apply_btn.config(state="normal")

    def log(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MigrationToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
