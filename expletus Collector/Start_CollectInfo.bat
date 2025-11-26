@echo off
set "SCRIPT=%~dp0Collect-Info_Progress.ps1"

REM Zuerst PowerShell 7 versuchen, sonst Windows PowerShell nutzen
set "PWSH=%ProgramFiles%\PowerShell\7\pwsh.exe"
if exist "%PWSH%" (
  "%PWSH%" -NoLogo -NoProfile -ExecutionPolicy Bypass -STA -File "%SCRIPT%"
) else (
  powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -STA -File "%SCRIPT%"
)
