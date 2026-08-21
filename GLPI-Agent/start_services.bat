@echo off
REM GLPI Agent - Servicio Principal
REM Este archivo inicia el Scheduler y Bot Interactivo

setlocal enabledelayedexpansion
set PYTHONIOENCODING=utf-8

cd /d "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"

REM Ejecutar con PowerShell (sin ventana visible)
powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "run_services.ps1"
