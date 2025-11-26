# APPLY Changelog

## Version 2.2 (2025-11-26)

### ✅ Abgeschlossene Aufgaben aus anweisungen.md

1. **Tool-Name geändert**
   - Von "COLLECT Configuration Migration Tool" zu "APPLY"
   - Anpassungen in start.bat und start.sh
   - Konsistente Namensgebung durchgängig

2. **eXpletus Design übernommen**
   - Vollständige Migration auf CustomTkinter
   - expletus_style.py integriert
   - Logo und Media-Files eingefügt
   - Moderne, einheitliche GUI im Dark Theme

3. **Features auf Liste reduziert**
   - Nur noch relevante Features gemäß docs/Liste Features JSON Export für APPLY.md:
     * Hostname
     * Benutzername
     * Domäne/Arbeitsgruppe
     * IPv4-Netzwerk (IP, DNS, Gateway)
     * Ständige Routen IPv4
     * Netzlaufwerke
     * Standard-Browser/PDF/Mail/Word-Anwendungen
     * Browser-Favoriten
     * MoBackup-Integration
   - Alte Features (ALBIS-Registry, Services, Files, etc.) entfernt

4. **APPLY_SKRIPT Ordner erstellt**
   - Fertige Dateien werden nicht mehr als ZIP gepackt
   - Alle benötigten Files in APPLY_SKRIPT/:
     * Python-Scripts (main.py, gui.py, config_applier.py, collect_parser.py)
     * Style (expletus_style.py)
     * Start-Scripts (start.bat, start.sh)
     * Assets (MoBackup unter assets/Mobackup/)
     * Media (Logo unter media/)
     * Dokumentation (README.md, requirements.txt)

5. **Backup-Funktion implementiert**
   - Automatisches Backup vor Änderungen
   - Checkbox in GUI zum Aktivieren/Deaktivieren
   - Backup-Verzeichnis: APPLY_Backup_<Zeitstempel>/
   - Sicherung von:
     * Registry-Keys
     * Hostname
     * Netzwerkkonfigurationen

6. **MoBackup-Integration**
   - MoBackup-Button in GUI (wird automatisch angezeigt wenn MoBackup-Einträge in JSON)
   - Start von MoBackup über GUI möglich
   - assets/Mobackup/ Ordner mit portabler Version integriert
   - Windows-spezifische Funktion

7. **Bug-Fix: Änderungen werden angewendet**
   - ConfigApplier komplett überarbeitet
   - Echte Implementierung für alle Features (nicht nur Dry-Run)
   - Windows-spezifische Befehle (netsh, wmic, route, etc.)
   - Korrekte Fehlerbehandlung

### Neue Features

- **Progress Bar**: Visueller Fortschritt während Migration
- **Status Label**: Echtzeit-Anzeige des aktuellen Vorgangs
- **Stop-Button**: Migration kann abgebrochen werden
- **Threaded Execution**: GUI bleibt responsiv während Migration
- **Scrollable Config List**: Alle Konfigurationen übersichtlich darstellbar
- **System-Info-Anzeige**: Quellsystem-Informationen werden angezeigt

### Technische Verbesserungen

- Migration auf CustomTkinter (modernes UI-Framework)
- Konsistentes eXpletus-Branding
- Verbesserte Fehlerbehandlung
- Backup-System vor Änderungen
- Windows-spezifische Implementierungen für:
  * Hostname-Änderung (wmic)
  * Netzwerkkonfiguration (netsh)
  * Persistente Routen (route -p)
  * Netzlaufwerke (net use)
  * Arbeitsgruppe (wmic)

### Dateien im APPLY_SKRIPT Ordner

```
APPLY_SKRIPT/
├── main.py                  # Einstiegspunkt
├── gui.py                   # GUI mit CustomTkinter
├── config_applier.py        # Konfiguration anwenden
├── collect_parser.py        # JSON-Parser
├── expletus_style.py        # eXpletus Design-System
├── requirements.txt         # Dependencies (customtkinter, pillow)
├── start.bat               # Windows Start-Script
├── start.sh                # Linux/Mac Start-Script
├── example_collect_data.json  # Beispieldaten
├── README.md               # Dokumentation
├── media/                  # Logo und Grafiken
│   └── expletus_1.png
└── assets/                 # MoBackup
    └── Mobackup/
        └── mobackup.exe
```

### Installation & Start

**Windows:**
```cmd
cd APPLY_SKRIPT
start.bat
```

**Linux/Mac:**
```bash
cd APPLY_SKRIPT
./start.sh
```

### Systemanforderungen

- Python 3.7+
- Windows (für alle Features) oder Linux/Mac (eingeschränkt)
- Admin-Rechte für Systemänderungen
- Abhängigkeiten: customtkinter, pillow (werden automatisch installiert)

### Bekannte Einschränkungen

- Einige Features funktionieren nur unter Windows
- Domänenbeitritt erfordert Credentials (manuelle Konfiguration)
- Standard-Anwendungen erfordern Registry-Änderungen
- Browser-Favoriten erfordern SQLite-Konvertierung (noch nicht implementiert)

### Nächste Schritte

- [ ] SQLite-Konvertierung für Browser-Favoriten
- [ ] Linux/Mac Unterstützung erweitern
- [ ] Automatische Registry-Änderungen für Standard-Apps
- [ ] Domänenbeitritt mit Credential-Handling
