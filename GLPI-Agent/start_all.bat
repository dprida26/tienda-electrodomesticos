@echo off
REM GLPI Agent - Inicia todos los servicios

setlocal enabledelayedexpansion
set PYTHONIOENCODING=utf-8

cd /d "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"

REM Ejecutar PowerShell con el script
powershell -NoProfile -ExecutionPolicy Bypass -File "start_all.ps1"

pause
