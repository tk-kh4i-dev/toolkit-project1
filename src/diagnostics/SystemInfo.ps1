<#
.SYNOPSIS
    [Brief description of what the script does]
.DESCRIPTION
    [A slightly more detailed explanation of the script's intent]
.LICENSE
    MIT License - See the LICENSE file in the root directory.
#>

Write-Host "--- System Overview ---" -ForegroundColor Cyan
Get-ComputerInfo | Select-Object OsName, OsVersion, OsBuildNumber, CsModel, CsTotalPhysicalMemory | Format-List

Write-Host "`n--- Current Memory Usage ---" -ForegroundColor Cyan
Get-Counter '\Memory\Available MBytes'


Write-Host "`nPress Enter to close this window..." -ForegroundColor Yellow
Read-Host