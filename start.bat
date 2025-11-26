@echo off
REM ###########################################################################
REM APPLY - Configuration Migration Tool - Start Script (Windows)
REM
REM Dieses Skript prueft alle Abhaengigkeiten und installiert fehlende
REM ###########################################################################

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ===============================================================
echo   APPLY - Configuration Migration Tool
echo   Startup Check
echo ===============================================================
echo.

REM ===== 1. Check Python installation =====
echo [1/5] Pruefe Python Installation...

set "PYTHON_CMD="
set "PYTHON_VERSION="

REM Method 1: Try 'py -3' (Windows Python Launcher - most reliable)
py -3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=py -3"
    for /f "tokens=2" %%v in ('py -3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    goto :python_found
)

REM Method 2: Try 'python' and check if it's Python 3
python --version >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
        set "PYTHON_VERSION=%%v"
        echo %%v | findstr /b "3." >nul
        if !errorlevel! equ 0 (
            set "PYTHON_CMD=python"
            goto :python_found
        )
    )
)

REM Method 3: Try 'python3'
python3 --version >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python3"
    for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    goto :python_found
)

REM ===== Python NOT found - try to install =====
echo [WARN] Python 3 nicht gefunden!
echo.

REM Try winget installation
where winget >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] Versuche Python automatisch zu installieren via winget...
    echo.
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    if !errorlevel! equ 0 (
        echo.
        echo [OK] Python wurde installiert!
        echo.
        echo ============================================================
        echo   WICHTIG: Bitte dieses Fenster SCHLIESSEN und
        echo            start.bat ERNEUT ausfuehren!
        echo ============================================================
        echo.
        pause
        exit /b 0
    )
    echo [WARN] Automatische Installation fehlgeschlagen.
    echo.
)

REM Manual installation instructions
echo ===============================================================
echo   PYTHON INSTALLATION ERFORDERLICH
echo ===============================================================
echo.
echo Python 3 wurde nicht gefunden und konnte nicht automatisch
echo installiert werden.
echo.
echo Bitte Python manuell installieren:
echo.
echo   1. Browser oeffnen: https://www.python.org/downloads/
echo.
echo   2. "Download Python 3.x" klicken
echo.
echo   3. Installer ausfuehren - WICHTIG:
echo.
echo      [x] "Add Python to PATH" ANKREUZEN! (ganz unten)
echo      [x] "Install Now" klicken
echo.
echo   4. Nach Installation:
echo      - Dieses Fenster schliessen
echo      - NEUES CMD-Fenster oeffnen
echo      - start.bat erneut ausfuehren
echo.
echo ===============================================================
echo.
pause
exit /b 1

:python_found
echo [OK] Python !PYTHON_VERSION! gefunden
echo      Befehl: !PYTHON_CMD!

REM ===== 2. Check tkinter =====
echo.
echo [2/5] Pruefe tkinter (GUI)...

!PYTHON_CMD! -c "import tkinter" >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] tkinter nicht verfuegbar!
    echo.
    echo tkinter ist Teil der Standard-Python-Installation.
    echo Bitte Python neu installieren und dabei "tcl/tk and IDLE" auswaehlen.
    echo.
    pause
    exit /b 1
)
echo [OK] tkinter verfuegbar

REM ===== 3. Check required files =====
echo.
echo [3/5] Pruefe Programm-Dateien...

set "FILES_OK=1"
if not exist "main.py" (
    echo [ERROR] main.py fehlt!
    set "FILES_OK=0"
)
if not exist "gui.py" (
    echo [ERROR] gui.py fehlt!
    set "FILES_OK=0"
)
if not exist "config_applier.py" (
    echo [ERROR] config_applier.py fehlt!
    set "FILES_OK=0"
)
if not exist "collect_parser.py" (
    echo [ERROR] collect_parser.py fehlt!
    set "FILES_OK=0"
)

if "!FILES_OK!" == "0" (
    echo.
    echo Bitte start.bat aus dem APPLY-Verzeichnis ausfuehren.
    pause
    exit /b 1
)
echo [OK] Alle Programm-Dateien vorhanden

REM ===== 4. Check Python modules =====
echo.
echo [4/5] Pruefe Python-Module...

!PYTHON_CMD! -c "import json, os, subprocess, pathlib, typing, threading, platform" >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Standard-Module fehlen!
    echo Bitte Python neu installieren.
    pause
    exit /b 1
)
echo [OK] Alle Module verfuegbar

REM ===== 5. Check optional files =====
echo.
echo [5/5] Pruefe optionale Dateien...

if exist "example_collect_data.json" (
    echo [OK] Beispieldaten vorhanden
) else (
    echo [INFO] Beispieldaten nicht vorhanden ^(optional^)
)

REM ===== All checks passed =====
echo.
echo ===============================================================
echo   Alle Pruefungen erfolgreich!
echo ===============================================================
echo.
echo   Python:      !PYTHON_VERSION!
echo   Verzeichnis: %CD%
echo   Hostname:    %COMPUTERNAME%
echo.
echo ---------------------------------------------------------------
echo   Starte APPLY...
echo ---------------------------------------------------------------
echo.

REM Start the application
!PYTHON_CMD! main.py
set "EXIT_CODE=!errorlevel!"

if !EXIT_CODE! equ 0 (
    echo.
    echo [OK] APPLY wurde beendet.
) else (
    echo.
    echo [ERROR] APPLY wurde mit Fehlercode !EXIT_CODE! beendet.
    pause
)

exit /b !EXIT_CODE!
