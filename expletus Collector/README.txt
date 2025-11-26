SCRIPTTHE Collect Info Package

FILES
- Start_CollectInfo.bat
- Collect-Info_Progress.ps1
- README.txt

USAGE
1) Put all files in the same folder.
2) Double-click Start_CollectInfo.bat (this suppresses the PowerShell welcome banner via -NoLogo).
3) The script creates a folder on Desktop named CollectInfo_YYYYMMDD_HHMMSS.
4) Outputs:
   - 00_baseinfo.txt
   - 01_network_ipconfig.txt
   - 02_printers.txt
   - 03_processes.txt
   - 04_systeminfo.txt
   - 05_REG_HKCU_Software_ALBIS.reg
   - 06_screenshot_YYYYMMDD_HHMMSS.png
   - 07_ALBISWIN (if any known ALBISWIN path exists)
NOTE
- A single GUI window now shows combined copy progress for ALBIS files and user folders.
