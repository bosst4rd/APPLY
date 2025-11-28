

- [x] das tool heisst apply, auch im startupcheck ändern,
- [x] folgendes Problem hast du super ausgemerzt bei dem repo COLLECT GUI, bitte ebenso fixen:
- [x] das design vom Repo COLLECT_GUI übernehmen - dazu habe ich dir die konfigdatei usw abgelegt in root\gui_design
- [x] die fertigen files nicht mehr als zip packen., sondern in einen Ordner im repo ablegen ("APPLY_SKRIPT")
- [x] ich habe dir eine Liste zur Verfügung gestellt unter \docs\ , diese Dinge sollen übernommen werden können der Rest braucht nicht dargestellt werden
- [x] es wird NICHTS von den angehakten Dingen übernommen, er sagt nur 6 Elemente verarbeitet... hat aber nichts geändert kein Dry Run!
- [x] unter \assets\ liegt die Software MoBackup(portabel), wenn die JSON den entsprechenden Eintrag enthält (Outlook-Backup z.B.) dann soll das Tool über die GUI gestartet werden können
- [x] die software soll fester bestandteil von APPLY werden ist es sinnvoll diese software (mobackup) in die base zu integrieren? oder einfach nur den ordner immer mitnehmen? -> Ordner wird immer mitgenommen in APPLY_SKRIPT/assets/
- [x] Backup vor start von Änderungen einbauen, um (wiederherstellbare) Konfigurationen notfalls wiederherzustellen 
- [ ] 
===============================================================
  APPLY
  Startup Check
===============================================================

[1/5] Pruefe Python Installation...
[OK] Python 3.11.9 gefunden
     Befehl: py -3

[2/5] Pruefe tkinter (GUI)...
[OK] tkinter verfuegbar

[3/5] Pruefe Programm-Dateien...
[OK] Alle Programm-Dateien vorhanden

[4/5] Pruefe Python-Module...
[OK] Alle Module verfuegbar

[5/5] Pruefe optionale Dateien...
[OK] Beispieldaten vorhanden

===============================================================
  Alle Pruefungen erfolgreich
===============================================================

  Python:      3.11.9
  Verzeichnis: C:\Users\Max Mustermann\Desktop\APPLY_SKRIPT
  Hostname:    DESKTOP-8J1V6EM

---------------------------------------------------------------
  Starte eXpletus APPLY...
---------------------------------------------------------------

Traceback (most recent call last):
  File "C:\Users\Max Mustermann\Desktop\APPLY_SKRIPT\main.py", line 11, in <module>
    from gui import main
  File "C:\Users\Max Mustermann\Desktop\APPLY_SKRIPT\gui.py", line 14, in <module>
    from config_applier import ConfigApplier
  File "C:\Users\Max Mustermann\Desktop\APPLY_SKRIPT\config_applier.py", line 48
    backup_file = self.backup_dir / f"registry_{key_path.replace('\\', '_').replace(':', '')}.reg"
                                                                                                  ^
SyntaxError: f-string expression part cannot include a backslash

[ERROR] APPLY wurde mit Fehlercode 1 beendet.
Drücken Sie eine beliebige Taste . . .
