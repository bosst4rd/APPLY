# COLLECT Configuration Migration Tool

Ein benutzerfreundliches GUI-Tool zur Migration von Systemkonfigurationen, die mit dem COLLECT-Tool gesammelt wurden, auf neue Hardware.

## Überblick

Dieses Tool ermöglicht es Ihnen:
- COLLECT-Konfigurationsdateien zu laden und zu analysieren
- Konfigurationen interaktiv auszuwählen, die migriert werden sollen
- Konfigurationen auf einem neuen System anzuwenden
- Den gesamten Prozess in einem Dry-Run-Modus zu testen

## Features

- **Benutzerfreundliche GUI**: Intuitive grafische Oberfläche mit tkinter und Checkboxen
- **Selektive Migration**: Wählen Sie mit Checkboxen genau aus, welche Konfigurationen angewendet werden sollen
- **ALBIS-Unterstützung**: Spezielle Unterstützung für ALBIS-Registry-Einträge
- **Übersichtliche Darstellung**: Kategorisierte Anzeige mit Icons und Beschreibungen
- **Software-Installation**: Installierte Software wird aufgelistet und kann zur Installation vorgemerkt werden
- **Dry-Run-Modus**: Testen Sie die Migration ohne tatsächliche Änderungen am System
- **Fortschrittsanzeige**: Echtzeit-Feedback über den Migrationsprozess
- **Ausführliches Logging**: Detaillierte Logs aller durchgeführten Aktionen
- **Fehlerbehandlung**: Robuste Fehlerbehandlung mit klaren Fehlermeldungen

## Unterstützte Konfigurationskategorien

1. **Hostname**: Systemhostname
2. **Netzwerk**: Netzwerkschnittstellen, IP-Adressen, DNS-Einstellungen
3. **ALBIS-Registry**: ALBIS-spezifische Registry-Einträge (Datenbankpfad, Lizenz, Ports, etc.)
4. **Benutzer**: Benutzerkonten, Gruppen, Home-Verzeichnisse
5. **Pakete**: Installierte Softwarepakete (mit Installationsoptionen)
6. **Dienste**: Systemdienste und deren Status
7. **Dateien**: Konfigurationsdateien und Verzeichnisse

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- tkinter (normalerweise in Python enthalten)

**📘 Detaillierte Python-Installationsanleitung:** Siehe [INSTALL_PYTHON.md](INSTALL_PYTHON.md)

> **Hinweis:** Die Start-Skripte (`start.sh` / `start.bat`) erkennen automatisch, ob Python korrekt installiert ist und geben hilfreiche Installationshinweise!

### Installation auf Ubuntu/Debian

```bash
# Python und tkinter installieren (falls nicht vorhanden)
sudo apt-get update
sudo apt-get install python3 python3-tk

# Repository klonen oder herunterladen
git clone <repository-url>
cd APPLY

# Optional: Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren (minimal)
pip install -r requirements.txt

# Tool mit automatischer Prüfung starten
./start.sh
```

### Installation auf anderen Systemen

**Windows:**
```batch
REM Python 3 von python.org herunterladen und installieren
REM WICHTIG: "Add Python to PATH" während Installation aktivieren!
REM tkinter ist normalerweise bereits enthalten

REM In das Projektverzeichnis wechseln
cd APPLY

REM Mit automatischer Prüfung starten (EMPFOHLEN)
start.bat

REM Oder direkt ausführen
python main.py
```

**macOS:**
```bash
# Python 3 installieren (falls nicht vorhanden)
brew install python3

# In das Projektverzeichnis wechseln
cd APPLY

# Mit automatischer Prüfung starten (EMPFOHLEN)
./start.sh

# Oder direkt ausführen
python3 main.py
```

## Verwendung

### 1. Tool starten

**EMPFOHLEN: Mit automatischer Abhängigkeitsprüfung**

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

Das Start-Skript prüft automatisch:
- ✓ Python-Installation und Version (≥3.7)
- ✓ tkinter (GUI-Bibliothek)
- ✓ Alle benötigten Python-Module
- ✓ Verfügbarkeit aller Projektdateien
- ✓ Display/GUI-Verfügbarkeit
- ✓ Gibt hilfreiche Fehlermeldungen bei Problemen

**Alternativ: Direkt starten (ohne Checks)**

```bash
python3 main.py
```

oder ausführbar machen:

```bash
chmod +x main.py
./main.py
```

### 2. COLLECT-Datei laden

1. Klicken Sie auf "Durchsuchen..." um eine COLLECT JSON-Datei auszuwählen
2. Klicken Sie auf "Laden" um die Datei zu laden
3. Die Konfigurationen werden in der Baumansicht angezeigt

### 3. Konfigurationen auswählen

- Jede Konfiguration hat eine eigene Checkbox
- Standardmäßig sind alle Konfigurationen ausgewählt
- **Kategorien**:
  - 🖥️ **Hostname**: Originalname des Systems
  - 🌐 **Netzwerk**: Netzwerkinterfaces (LAN, WAN, etc.)
  - 📝 **ALBIS-Registry**: Registry-Einträge (Datenbankpfad, Lizenz, Server-Port, etc.)
  - 👤 **Benutzernamen**: Benutzerkonten und Gruppen
  - 📦 **Installierte Software**: Mit Option zur Installation
  - ⚙️ **Dienste**: Systemdienste
  - 📁 **Dateien**: Konfigurationsdateien
- Verwenden Sie "Alle auswählen" / "Alle abwählen" für schnelle Auswahl
- Scrollen Sie durch die Liste um alle Optionen zu sehen

### 4. Optionen festlegen

- **Dry Run**: Aktiviert (Standard) - Nur simulieren, keine Änderungen
- Deaktivieren Sie Dry Run nur, wenn Sie sicher sind!

### 5. Migration durchführen

1. Klicken Sie auf "Konfigurationen anwenden"
2. Bei deaktiviertem Dry Run erhalten Sie eine Sicherheitswarnung
3. Verfolgen Sie den Fortschritt im Log-Bereich
4. Nach Abschluss erhalten Sie eine Zusammenfassung

## COLLECT-Dateiformat

Die COLLECT-Datei muss im JSON-Format vorliegen:

```json
{
  "system_info": {
    "hostname": "old-albis-server",
    "os": "Windows Server 2019",
    "albis_version": "ALBIS 5.2",
    "collection_date": "2025-11-15T10:30:00Z"
  },
  "configurations": {
    "hostname": {
      "value": "old-albis-server",
      "description": "Original hostname"
    },
    "network": {
      "LAN": {
        "description": "Primäre Netzwerkschnittstelle",
        "interface": "LAN",
        "ip_address": "192.168.1.100",
        "netmask": "255.255.255.0"
      }
    },
    "albis_registry": {
      "database_path": {
        "description": "ALBIS Datenbankpfad",
        "key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\ALBIS\\Database\\Path",
        "value": "C:\\ALBIS\\Database",
        "type": "string"
      }
    },
    "users": {
      "albis_admin": {
        "description": "ALBIS Administrator",
        "username": "albis_admin",
        "groups": ["Administrators", "ALBIS_Admins"]
      }
    },
    "packages": {
      "albis_components": {
        "description": "ALBIS Komponenten",
        "packages": ["ALBIS Server 5.2", "ALBIS Client 5.2"]
      }
    }
  }
}
```

Eine vollständige Beispieldatei mit ALBIS-Konfigurationen finden Sie in `example_collect_data.json`.

## Sicherheitshinweise

⚠️ **WICHTIG**: Dieses Tool kann signifikante Änderungen am System vornehmen!

### Vor der Verwendung

1. **Backup erstellen**: Erstellen Sie ein vollständiges Backup des Zielsystems
2. **Dry Run testen**: Führen Sie IMMER zuerst einen Dry Run durch
3. **Logs überprüfen**: Überprüfen Sie die Logs auf potenzielle Probleme
4. **Berechtigungen**: Stellen Sie sicher, dass Sie die nötigen Rechte haben

### Best Practices

- Testen Sie auf einem Test-System vor der Produktions-Migration
- Dokumentieren Sie alle Änderungen
- Führen Sie die Migration außerhalb der Produktionszeiten durch
- Halten Sie das COLLECT-Tool und dieses Tool auf dem aktuellen Stand

## Architektur

Das Tool besteht aus drei Hauptkomponenten:

### 1. CollectParser (`collect_parser.py`)
- Lädt und parst COLLECT JSON-Dateien
- Extrahiert Systeminfo und Konfigurationskategorien
- Stellt strukturierten Zugriff auf Konfigurationsdaten bereit

### 2. ConfigApplier (`config_applier.py`)
- Wendet Konfigurationen auf das System an
- Unterstützt Dry-Run-Modus
- Bietet kategoriespezifische Applier-Funktionen
- Erstellt detaillierte Logs und Fehlerberichte

### 3. GUI (`gui.py`)
- Benutzerfreundliche grafische Oberfläche
- Interaktive Auswahl von Konfigurationen
- Echtzeit-Fortschritt und Logging
- Thread-basierte Ausführung für responsive UI

## Erweiterung

### Neue Konfigurationskategorie hinzufügen

1. Fügen Sie eine neue Applier-Methode in `config_applier.py` hinzu:

```python
def apply_custom_config(self, config: Dict[str, Any]) -> Tuple[bool, str]:
    """Apply custom configuration"""
    try:
        # Ihre Implementierung hier
        return True, "Success message"
    except Exception as e:
        return False, f"Error: {str(e)}"
```

2. Registrieren Sie die Methode im `appliers` Dictionary:

```python
appliers = {
    'network': self.apply_network_config,
    'users': self.apply_user_config,
    'custom': self.apply_custom_config,  # Neu
}
```

## Fehlerbehebung

### Start-Skript verwenden für Diagnose
Das Start-Skript (`start.sh` / `start.bat`) erkennt die meisten Probleme automatisch:

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

### Häufige Probleme

**"Modul tkinter nicht gefunden"**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Windows
# Reinstall Python from python.org with "tcl/tk and IDLE" option enabled
```

**"Python nicht gefunden" (Windows oder Linux)**
- **Lösung:** Siehe [INSTALL_PYTHON.md](INSTALL_PYTHON.md) für vollständige Installationsanleitung
- Windows: Python wurde nicht zu PATH hinzugefügt
- Neuinstallation mit "Add Python to PATH" Option
- Das Start-Skript findet automatisch `python`, `python3` oder `py -3`

**"Keine Berechtigung zum Ändern der Konfiguration"**
- Das GUI-Tool selbst benötigt KEINE Admin-Rechte
- Admin-Rechte werden bei Bedarf während der Migration angefordert
- Führen Sie das Start-Skript als normaler Benutzer aus

**GUI startet nicht**
- Start-Skript prüft automatisch Display-Verfügbarkeit
- Bei SSH-Verbindungen: Verwenden Sie X11-Forwarding (`ssh -X`)
- Oder verwenden Sie VNC/Remote Desktop

**"Datei nicht gefunden"**
- Stellen Sie sicher, dass Sie im APPLY-Verzeichnis sind
- Start-Skript prüft automatisch alle benötigten Dateien

## Entwicklung

### Tests durchführen

```bash
# Mit Beispieldatei testen
python3 main.py
# Dann example_collect_data.json laden
```

### Code-Struktur

```
APPLY/
├── main.py                      # Einstiegspunkt
├── gui.py                       # GUI-Anwendung
├── collect_parser.py            # Parser für COLLECT-Daten
├── config_applier.py            # Konfiguration-Anwendung
├── example_collect_data.json    # Beispieldatei
├── requirements.txt             # Abhängigkeiten
└── README.md                    # Diese Datei
```

## Lizenz

[Lizenz hier einfügen]

## Support

Bei Fragen oder Problemen:
- Erstellen Sie ein Issue im Repository
- Überprüfen Sie die Logs für detaillierte Fehlermeldungen
- Konsultieren Sie die COLLECT-Tool-Dokumentation

## Changelog

### Version 2.1.0 (2025-11-15)
- **NEU**: Automatische Start-Skripte mit Abhängigkeitsprüfung
  * `start.sh` für Linux/Mac
  * `start.bat` für Windows
- **NEU**: Prüfung von Python-Version (≥3.7)
- **NEU**: Automatische tkinter-Erkennung
- **NEU**: Display-Verfügbarkeits-Check
- **NEU**: Hilfreiche Fehlermeldungen mit Lösungsvorschlägen
- Verbesserte Dokumentation mit Installations- und Fehlerbehandlungshinweisen

### Version 2.0.0 (2025-11-15)
- **NEU**: Checkbox-basierte Auswahl für jede einzelne Konfiguration
- **NEU**: ALBIS-Registry Unterstützung
- **NEU**: Hostname-Konfiguration
- **NEU**: Verbesserte GUI mit Icons und Kategorien
- **NEU**: Scrollbare Konfigurationsliste
- **NEU**: Software-Installationsoptionen mit Paketlisten
- Verbesserte Benutzerführung mit deutschen Beschreibungen
- Angepasste Beispieldaten für ALBIS-Systeme

### Version 1.0.0 (2025-11-15)
- Erste Version
- Unterstützung für Netzwerk, Benutzer, Pakete, Dienste und Dateien
- GUI mit tkinter
- Dry-Run-Modus
- Ausführliches Logging

## TODO / Geplante Features

- [ ] Import/Export von Migrations-Profilen
- [ ] Rollback-Funktionalität
- [ ] Automatische Backups vor Migration
- [ ] CLI-Modus für Skript-Automatisierung
- [ ] Unterstützung für weitere Konfigurationskategorien
- [ ] Multi-System-Migration (Batch-Verarbeitung)
- [ ] Konfigurationsvalidierung vor Anwendung
- [ ] Detaillierte Diff-Ansicht
- [ ] Plugin-System für benutzerdefinierte Applier

## Beiträge

Beiträge sind willkommen! Bitte:
1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Erstellen Sie einen Pull Request

---

**Warnung**: Dieses Tool ist in der Entwicklung. Verwenden Sie es mit Vorsicht in Produktionsumgebungen!
