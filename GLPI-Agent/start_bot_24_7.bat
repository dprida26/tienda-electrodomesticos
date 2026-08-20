@echo off
REM Script para iniciar el GLPI Bot 24/7 con reinicio automático

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ================================================
echo GLPI Bot 24/7 - Auto Restart
echo ================================================
echo.
echo Location: %CD%
echo.

set MAX_FAILURES=5
set RESTART_DELAY=5
set FAILURE_COUNT=0

:loop

echo [%date% %time%] Attempting to start bot (Attempt !FAILURE_COUNT! of %MAX_FAILURES%)
echo.

python bot_24_7.py

set /a FAILURE_COUNT+=1

if %FAILURE_COUNT% geq %MAX_FAILURES% (
    echo.
    echo [ERROR] Bot failed %MAX_FAILURES% times in a row
    echo Waiting 60 seconds before retry...
    echo.
    timeout /t 60 /nobreak
    set FAILURE_COUNT=0
)

echo Restarting in %RESTART_DELAY% seconds...
timeout /t %RESTART_DELAY% /nobreak

goto loop
