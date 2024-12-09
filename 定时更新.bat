@echo off
:loop

taskkill /F /IM python.exe
git fetch --all
git reset --hard origin/main
git pull
.\BLprint_nogui.exe

timeout /t 86400

goto loop