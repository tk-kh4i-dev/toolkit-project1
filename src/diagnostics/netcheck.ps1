<#
.SYNOPSIS
    Scans for active network traffic on the machine 
.DESCRIPTION
    Scans for active network traffic and its IP, ports.
.LICENSE
    MIT License - See the LICENSE file in the root directory.
#>

Write-Host "Active Network Connections:" -ForegroundColor Green
Get-NetTCPConnection | Where-Object { $_.State -eq 'Established' } | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort | Format-Table -AutoSize


Write-Host "`nPress Enter to close this window..." -ForegroundColor Yellow
Read-Host