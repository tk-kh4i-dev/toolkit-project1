# toolbox.ps1
# This script acts as a hub for your toolkit. 
# It makes your scripts real-life applicable by presenting them as a menu.
<#
.SYNOPSIS
    Command Center to execute other files in the folder.
.DESCRIPTION
    Usage: for a more straightforward way to use the included scripts.
.LICENSE
    MIT License - See the LICENSE file in the root directory.
#>

$baseDir = $PSScriptRoot
$srcDir = "$baseDir\src"

# Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] ERROR: 'python.exe' not found in your system PATH." -ForegroundColor Red
    Write-Host "[!] Please install Python via 'https://python.org/downloads/' and add it to your PATH." -ForegroundColor Yellow
    Pause
    exit
} else {
    $pythonPath = (Get-Command python).Source
    Write-Host "[+] Environment Ready: Using Python at $pythonPath" -ForegroundColor Green
}

$cleaner = "$srcDir\maintenance\disk_clean.py"
$scanner = "$srcDir\diagnostics\file_scan.py"
$netcheck = "$srcDir\diagnostics\netcheck.ps1"
$sysinfo = "$srcDir\diagnostics\sys_info.py"

while ($true) {
    Clear-Host
    $HostName = $env:COMPUTERNAME
    Write-Host "`n--- $HostName System Toolkit ---" -ForegroundColor Cyan
    Write-Host "1. Clean temporary files"
    Write-Host "2. Scan files, count & find duplicates of them"
    Write-Host "3. Scan network traffic"
    Write-Host "4. Display system information & resources"
    Write-Host "q. Quit"
    
    $choice = Read-Host "Select an option"
    
    switch ($choice) {
        '1' { 
            Write-Host "Running Disk Cleaner ..." -ForegroundColor Gray
            & python $cleaner; Pause 
        }
        '2' { 
            Write-Host "Running File Scanner ..." -ForegroundColor Gray
            & python $scanner; Pause 
        } 
        '3' { 
            Write-Host "Running Network Traffic Scanner ..." -ForegroundColor Gray
            & powershell -File $netcheck; Pause 
        }
        '4' { 
            Write-Host "Retrieving System Information ..." -ForegroundColor Gray
            & python $sysinfo; Pause 
        }
        'q' { 
            Write-Host "Exiting Toolkit ..." -ForegroundColor Yellow
            return # To exit toolkit
         }
        default { 
            Write-Host "Invalid choice!" -ForegroundColor Red
            Pause
        }
    }
}
