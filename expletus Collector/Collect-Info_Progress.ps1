<# =====================================================================
  Skriptname: Collect-Info_MIN.ps1
  Milestone1+++++ | Stand: 12.09.2025
  
  Zweck:
    - Zielordner per Dialog waehlen; Unterordner = COMPUTERNAME (Hostname)
    - Basisinfos erfassen
    - Druckerliste bereinigt (Blacklist + Deduplizierung)
    - Registry-Export HKCU\Software\ALBIS → albis.reg
    - Kopieren:
        * ALBIS: nur Dateien aus C:\CGM\ALBISWIN → <Ziel>\ALBISWIN
        * Benutzerordner: Desktop, Dokumente, Bilder (aktuell auskommentiert!)
    - Netzwerk-Infos erfassen
    - Screenshot vom Desktop (desktop.png)
    - Fortschrittsanzeige: „Diagnose laeuft“
    - Abschluss: Explorer oeffnet Zielordner

  Enthaltene Features:
    - Feste Dateinamen/Struktur (Basisinfo.txt, Drucker.txt, Netzwerk.txt, albis.reg, desktop.png, \ALBISWIN)
===================================================================== #>

# --- Parameter / Quellen ---
$LocalAlbisPath      = "C:\CGM\ALBISWIN"
$AlbisDestFolderName = "ALBISWIN"

# --- Logging vorbereiten ---
$LogPath = Join-Path $env:TEMP "CollectInfo_last_run.log"
try { Stop-Transcript | Out-Null 2>$null } catch {}
Start-Transcript -Path $LogPath -Append -Force | Out-Null

# Schritte
$steps = @(
    "Zielordner vorbereiten",
    "Basis-Informationen erfassen",
    "Druckerliste erstellen",
    "Registry exportieren",
    "ALBIS-Dateien kopieren",
    #"Benutzerordner kopieren",   # aktuell auskommentiert
    "Netzwerk-Informationen erfassen",
    "Screenshot aufnehmen",
    "Abschluss"
)
$stepIndex = 0; $totalSteps = $steps.Count
function Show-Progress { param($activity, $status)
    $percent = [int](($stepIndex / $totalSteps) * 100)
    Write-Progress -Activity "Diagnose laeuft" -Status $status -PercentComplete $percent
}

Write-Host "`n=== Collect-Info_MIN | Milestone1+++++ gestartet ===" -ForegroundColor Cyan

# --- Zielordner vorbereiten ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
Add-Type -AssemblyName System.Windows.Forms
$desktop     = [Environment]::GetFolderPath("Desktop")
$dialog      = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description  = "Bitte Zielordner waehlen (es wird ein Unterordner = HOSTNAME angelegt)"
$dialog.SelectedPath = $desktop
$null  = $dialog.ShowDialog()
$chosen = if ($dialog.SelectedPath) { $dialog.SelectedPath } else { $desktop }
$DestRoot = Join-Path $chosen $env:COMPUTERNAME
New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null
Write-Host "Zielordner: $DestRoot" -ForegroundColor Yellow
Add-Type -AssemblyName System.Windows.Forms
$CopyUserFolders = $false
$dlg = [System.Windows.Forms.MessageBox]::Show(
    "Benutzerordner (Dokumente, Bilder, Desktop) mitkopieren?",
    "Benutzerordner kopieren",
    [System.Windows.Forms.MessageBoxButtons]::YesNo,
    [System.Windows.Forms.MessageBoxIcon]::Question
)
if ($dlg -eq [System.Windows.Forms.DialogResult]::Yes) { $CopyUserFolders = $true }
Write-Host "Es wurde der lokale Pfad C:\CGM\ALBISWIN ermittelt" -ForegroundColor Green

# --- Basis-Informationen ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$baseInfo = @(
    "Datum/Zeit:        $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    "Computername:      $env:COMPUTERNAME"
    "Benutzername:      $env:USERNAME"
    "Benutzer-Domaene:   $env:USERDOMAIN"
    "Computer-Domaene:   $((Get-CimInstance Win32_ComputerSystem).Domain)"
    "Seriennummer:      $((Get-CimInstance Win32_BIOS).SerialNumber)"
)
$baseInfoPath = Join-Path $DestRoot "Basisinfo.txt"
$baseInfo | Out-File -FilePath $baseInfoPath -Encoding UTF8 -Force
Write-Host "Basis-Infos -> $baseInfoPath" -ForegroundColor Green

# --- Druckerliste ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$PrinterBlacklistPatterns = @('^Fax$','^Microsoft XPS Document Writer$','^Microsoft Print to PDF$','^OneNote.*')
function Test-PrinterBlacklisted { param([string]$Name)
    foreach ($pat in $PrinterBlacklistPatterns) { if ($Name -match $pat) { return $true } }
    return $false
}
$printersRaw = Get-Printer | Select-Object Name, PortName, DriverName, Shared, Default
$filtered    = $printersRaw | Where-Object { -not (Test-PrinterBlacklisted -Name $_.Name) }
$seenNames = [System.Collections.Generic.HashSet[string]]::new()
$seenPorts = [System.Collections.Generic.HashSet[string]]::new()
$deduped   = [System.Collections.Generic.List[object]]::new()
foreach ($p in $filtered) {
    if (-not $seenNames.Contains($p.Name) -and -not $seenPorts.Contains($p.PortName)) {
        $null = $seenNames.Add($p.Name)
        if ($p.PortName) { $null = $seenPorts.Add($p.PortName) }
        $deduped.Add($p)
    }
}
$printersOutPath = Join-Path $DestRoot "Drucker.txt"
$lines = @("Name`tPort`tDefault`tShared`tTreiber")
$deduped | ForEach-Object { $lines += ("{0}`t{1}`t{2}`t{3}`t{4}" -f $_.Name, $_.PortName, $_.Default, $_.Shared, $_.DriverName) }
$lines | Out-File -FilePath $printersOutPath -Encoding UTF8 -Force
Write-Host "Drucker -> $printersOutPath" -ForegroundColor Green

# --- Registry ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$regOut = Join-Path $DestRoot "albis.reg"
Start-Process reg.exe -ArgumentList @("export","HKCU\Software\ALBIS",$regOut,"/y") -NoNewWindow -Wait
Write-Host "Registry-Export -> $regOut" -ForegroundColor Green

# --- ALBIS-Dateien (nur Dateien, keine Verzeichnisse) ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$DestAlbis = Join-Path $DestRoot $AlbisDestFolderName
New-Item -ItemType Directory -Path $DestAlbis -Force | Out-Null
Get-ChildItem -Path $LocalAlbisPath -File | Copy-Item -Destination $DestAlbis -Force
Write-Host "ALBIS-Dateikopie (ohne Verzeichnisse) -> $DestAlbis" -ForegroundColor Green

# --- Benutzerordner (gesamter Inhalt) kopieren ---
if ($CopyUserFolders) {
    $map = @(
        @{ name = 'Dokumente'; src = [Environment]::GetFolderPath('MyDocuments') }
        @{ name = 'Bilder';    src = [Environment]::GetFolderPath('MyPictures') }
        @{ name = 'Desktop';   src = [Environment]::GetFolderPath('Desktop') }
    )
    foreach ($m in $map) {
        if (-not [string]::IsNullOrWhiteSpace($m.src) -and (Test-Path -LiteralPath $m.src)) {
            $dst = Join-Path -Path $DestRoot -ChildPath $m.name
            New-Item -ItemType Directory -Path $dst -Force | Out-Null
& robocopy $m.src $dst /E /COPY:DAT /R:1 /W:1 /ETA /V /TEE
            Write-Host ("Benutzerordner kopiert -> {0}" -f $dst) -ForegroundColor Green
        }
    }
} else {
    Write-Host "Benutzerordner-Kopie uebersprungen (Auswahl: Nein)" -ForegroundColor Yellow
}
# --- Netzwerk ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$netzOut = Join-Path $DestRoot "Netzwerk.txt"
$netzLines = @()
$adapters = Get-NetAdapter | Sort-Object ifIndex
foreach ($a in $adapters) {
    $cfg  = Get-NetIPConfiguration -InterfaceIndex $a.ifIndex
    $ipv4 = ($cfg.IPv4Address        | ForEach-Object { $_.IPv4Address }) -join ", "
    $ipv6 = ($cfg.IPv6Address        | ForEach-Object { $_.IPv6Address }) -join ", "
    $gw   = ($cfg.IPv4DefaultGateway | ForEach-Object { $_.NextHop }) -join ", "
    $dns  = ($cfg.DnsServer.ServerAddresses) -join ", "
    $netzLines += "------------------------------------------------------------"
    $netzLines += "Adapter:  $($a.Name)"
    $netzLines += "Status:   $($a.Status)"
    $netzLines += "MAC:      $($a.MacAddress)"
    $netzLines += "IPv4:     $ipv4"
    $netzLines += "IPv6:     $ipv6"
    $netzLines += "Gateway:  $gw"
    $netzLines += "DNS:      $dns"
}
$netzLines | Out-File -FilePath $netzOut -Encoding UTF8 -Force
Write-Host "Netzwerk -> $netzOut" -ForegroundColor Green

# --- Screenshot ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
$shell = New-Object -ComObject "Shell.Application"
$shell.ToggleDesktop()   # Alle Fenster minimieren
Start-Sleep -Milliseconds 500
Add-Type -AssemblyName System.Drawing
$bounds   = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp      = New-Object Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.Size)
$shotOut  = Join-Path $DestRoot "desktop.png"
$bmp.Save($shotOut, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose(); $bmp.Dispose()
$shell.ToggleDesktop()   # Fenster wiederherstellen
Write-Host "Screenshot -> $shotOut" -ForegroundColor Green

# --- Abschluss ---
$stepIndex++; Show-Progress "Diagnose laeuft" $steps[$stepIndex-1]
Start-Process explorer.exe $DestRoot
Write-Host "`nFertig. Log: $LogPath" -ForegroundColor Cyan
Stop-Transcript | Out-Null
Write-Progress -Activity "Diagnose laeuft" -Completed
