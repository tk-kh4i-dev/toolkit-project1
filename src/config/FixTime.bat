:: NAME: FixTime.bat
:: DESCRIPTION: Can be used to force the machine to use NTP as its time source instead of CMOS, can be applied to machines that ran the command "/product server" on Windows installation.
:: LICENSE: MIT License - See the LICENSE file in the root directory.
@echo off
:: This script fixes the 'Local CMOS Clock' error on Server-bypassed Windows 11
echo ---------------------------------------
echo Kicking Windows Time Service into gear...
echo ---------------------------------------

:: Force the service to start if it crashed
net start w32time 2>nul

:: Set the Registry keys for NTP sync (Home PC style)
reg add "HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Parameters" /v Type /t REG_SZ /d NTP /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\W32Time\Config" /v AnnounceFlags /t REG_DWORD /d 5 /f

:: Force a rediscover and sync
w32tm /config /update
w32tm /resync /rediscover

echo ---------------------------------------
echo Done! Check your clock.
pause