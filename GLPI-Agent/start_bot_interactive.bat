@echo off
REM GLPI Agent - Bot Interactivo (Bajo demanda)

setlocal enabledelayedexpansion

REM Configurar encoding para Python
set PYTHONIOENCODING=utf-8

cd /d "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"

:start
echo.
echo GLPI BOT INTERACTIVO - Bajo Demanda
echo Iniciando... %date% %time%
echo.

python telegram_bot_interactive.py

REM Si falla, reintentar despues de 10 segundos
echo.
echo Servicio detenido. Reintentando en 10 segundos...
timeout /t 10 /nobreak
goto start
