<#
.SYNOPSIS
    For cleaning temporary files.
.DESCRIPTION
    Cleaning temporary files that have been staying in your temp folder for more than 7 days, you can change it back changing the value of line 11.
.LICENSE
    MIT License - See the LICENSE file in the root directory.
#>

$tempPath = "$env:TEMP"
$daysOld = 7
$cutoffDate = (Get-Date).AddDays(-$daysOld)

Write-Host "--- Temporary Files Cleaner ---" -ForegroundColor Cyan
$filesToDelete = Get-ChildItem -Path $tempPath -File | Where-Object { $_.LastWriteTime -lt $cutoffDate }

if ($filesToDelete) {
    foreach ($file in $filesToDelete) {
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction Stop
            Write-Host "Deleted: $($file.Name)" -ForegroundColor Green
        }
        catch {
            Write-Host "Could not delete: $($file.Name)" -ForegroundColor Red
        }
    }
}
else {
     Write-Host "No old temporary files found."
}

Write-Host "`nPress Enter to close this window..." -ForegroundColor Yellow
Read-Host