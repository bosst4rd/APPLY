@echo off
REM ###########################################################################
REM APPLY - Configuration Migration Tool - Build Script (Windows)
REM
REM Erstellt eine ZIP-Datei mit allen Dateien zum Testen
REM ###########################################################################

setlocal enabledelayedexpansion

echo ===============================================================
echo   APPLY - Configuration Migration Tool - Build Script
echo ===============================================================
echo.

REM Get current date and time for filename
for /f "tokens=1-3 delims=/" %%a in ("%date%") do (
    set DAY=%%a
    set MONTH=%%b
    set YEAR=%%c
)
for /f "tokens=1-2 delims=:" %%a in ("%time%") do (
    set HOUR=%%a
    set MINUTE=%%b
)
set HOUR=%HOUR: =0%

set TIMESTAMP=%YEAR%%MONTH%%DAY%_%HOUR%%MINUTE%
set VERSION=2.3.0

echo [INFO] Building release package...
echo [INFO] Version: %VERSION%
echo [INFO] Timestamp: %TIMESTAMP%
echo.

REM Check if releases folder exists
if not exist "releases" (
    echo [INFO] Creating releases folder...
    mkdir releases
)

REM Define output filename
set ZIPNAME=APPLY_v%VERSION%_%TIMESTAMP%.zip
set LATEST=APPLY_latest.zip

echo [INFO] Creating ZIP: %ZIPNAME%
echo.

REM Check if PowerShell is available (for ZIP creation)
where powershell >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] PowerShell not found!
    echo [ERROR] Please install PowerShell or use 7-Zip manually
    pause
    exit /b 1
)

REM Create temporary build directory
set BUILDDIR=%TEMP%\APPLY_build
if exist "%BUILDDIR%" rd /s /q "%BUILDDIR%"
mkdir "%BUILDDIR%"
mkdir "%BUILDDIR%\expletus Collector"

REM Copy main files
echo [INFO] Copying main files...
copy /Y main.py "%BUILDDIR%\" >nul
copy /Y gui.py "%BUILDDIR%\" >nul
copy /Y collect_parser.py "%BUILDDIR%\" >nul
copy /Y config_applier.py "%BUILDDIR%\" >nul
copy /Y example_collect_data.json "%BUILDDIR%\" >nul
copy /Y requirements.txt "%BUILDDIR%\" >nul
copy /Y start.bat "%BUILDDIR%\" >nul
copy /Y start.sh "%BUILDDIR%\" >nul

REM Copy documentation
if exist README.md copy /Y README.md "%BUILDDIR%\" >nul
if exist QUICKSTART.md copy /Y QUICKSTART.md "%BUILDDIR%\" >nul
if exist INSTALL_PYTHON.md copy /Y INSTALL_PYTHON.md "%BUILDDIR%\" >nul

REM Copy expletus Collector scripts
echo [INFO] Copying Collector scripts...
copy /Y "expletus Collector\*.*" "%BUILDDIR%\expletus Collector\" >nul

echo.
echo [INFO] Creating ZIP archive...

REM Create ZIP using PowerShell
powershell -Command "Compress-Archive -Path '%BUILDDIR%\*' -DestinationPath 'releases\%ZIPNAME%' -Force"

if %errorLevel% neq 0 (
    echo [ERROR] Failed to create ZIP file!
    rd /s /q "%BUILDDIR%"
    pause
    exit /b 1
)

REM Also create/update latest version
copy /Y "releases\%ZIPNAME%" "releases\%LATEST%" >nul

REM Cleanup
rd /s /q "%BUILDDIR%"

echo.
echo ===============================================================
echo   Build Complete!
echo ===============================================================
echo.
echo [OK] Created: releases\%ZIPNAME%
echo [OK] Updated: releases\%LATEST%
echo.
echo Included:
echo   - APPLY Tool (Python GUI)
echo   - expletus Collector (PowerShell Scripts)
echo   - Documentation
echo.

REM Show file size
for %%A in ("releases\%ZIPNAME%") do echo [INFO] Package size: %%~zA bytes
echo.

pause
