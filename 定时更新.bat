@echo off
:loop

taskkill /F /IM python.exe
git pull origin main
.\BLprint_nogui.exe

timeout /t 86400

goto loop