# Releases / Test-Builds

In diesem Ordner werden die ZIP-Pakete zum Testen abgelegt.

## Aktuelle Version

- **APPLY_latest.zip** - Immer die neueste Version
- **APPLY_v2.2.0_*.zip** - Versionierte Builds mit Timestamp

## Verwendung

1. **ZIP herunterladen oder extrahieren**
2. **In den extrahierten Ordner wechseln**
3. **Start-Skript ausführen:**

   **Windows:**
   ```batch
   start.bat
   ```

   **Linux/Mac:**
   ```bash
   ./start.sh
   ```

## Neuen Build erstellen

**Windows:**
```batch
build.bat
```

**Linux/Mac:**
```bash
./build.sh
```

Die Build-Skripte:
- Prüfen ob alle Dateien vorhanden sind
- Erstellen eine versionierte ZIP-Datei mit Timestamp
- Aktualisieren APPLY_latest.zip

## Enthaltene Dateien

Jedes ZIP enthält:

| Datei | Beschreibung |
|-------|--------------|
| `main.py` | Hauptprogramm (Einstiegspunkt) |
| `gui.py` | GUI-Anwendung |
| `collect_parser.py` | Parser für COLLECT-Daten |
| `config_applier.py` | Konfigurationsanwendung |
| `example_collect_data.json` | Beispieldatei zum Testen |
| `requirements.txt` | Python-Abhängigkeiten |
| `start.sh` | Linux/Mac Start-Skript |
| `start.bat` | Windows Start-Skript |
| `README.md` | Vollständige Dokumentation |
| `QUICKSTART.md` | Schnellstart-Anleitung |
| `INSTALL_PYTHON.md` | Python-Installationsanleitung |

## Hinweise

- Die Start-Skripte prüfen automatisch alle Abhängigkeiten
- Python 3.7+ und tkinter müssen installiert sein
- Bei Problemen: Siehe INSTALL_PYTHON.md
