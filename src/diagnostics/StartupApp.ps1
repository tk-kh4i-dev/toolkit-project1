<#
.SYNOPSIS
    To see what programs are set to start automatically.
.DESCRIPTION
    <none>
.LICENSE
    MIT License - See the LICENSE file in the root directory.
#>

Write-Host "Programs set to start automatically:" -ForegroundColor Yellow
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location | Format-Table -AutoSize


Write-Host "`nPress Enter to close this window..." -ForegroundColor Yellow
Read-Host