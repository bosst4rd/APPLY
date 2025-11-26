# eXpletus APPLY v2.2

Konfigurationsmigrations-Tool für Windows-Systeme.

## Schnellstart

### Windows
```cmd
start.bat
```

### Linux/Mac
```bash
./start.sh
```

## Features

- ✅ Hostname wiederherstellen
- ✅ Benutzername konfigurieren
- ✅ Domäne/Arbeitsgruppe einstellen
- ✅ IPv4-Netzwerkkonfiguration (IP, DNS, Gateway)
- ✅ Persistente Routen konfigurieren
- ✅ Netzlaufwerke mappen
- ✅ Standard-Anwendungen festlegen (Browser, PDF, Mail, Word)
- ✅ Browser-Favoriten importieren
- ✅ MoBackup-Integration für Outlook-Backups
- ✅ Automatisches Backup vor Änderungen
- ✅ Dry-Run-Modus zum Testen

## Voraussetzungen

- Python 3.7+
- Unter Windows: Admin-Rechte für Systemänderungen
- CustomTkinter und Pillow (werden automatisch installiert)

## Verwendung

1. Start-Skript ausführen (`start.bat` oder `start.sh`)
2. COLLECT JSON-Datei laden
3. Gewünschte Konfigurationen auswählen
4. Optional: Dry Run aktivieren (zum Testen)
5. "Anwenden" klicken

## MoBackup

Das Tool enthält MoBackup (portable Version) unter `assets/Mobackup/`.
Wenn die JSON-Datei Outlook-Backup-Einträge enthält, kann MoBackup über die GUI gestartet werden.

## Backup

Vor jeder Änderung (wenn "Backup erstellen" aktiviert ist) wird automatisch ein Backup erstellt:
- Registry-Keys werden exportiert
- Hostname wird gesichert
- Netzwerkkonfigurationen werden protokolliert

Backup-Ordner: `APPLY_Backup_<Zeitstempel>/`

## Sicherheitshinweise

⚠️ **WICHTIG:**
- Immer zuerst mit Dry Run testen!
- Backup des Zielsystems erstellen
- Admin-Rechte erforderlich für Systemänderungen
- Einige Änderungen erfordern Neustart

## Lizenz

© eXpletus - Alle Rechte vorbehalten
