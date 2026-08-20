@echo off
setlocal enabledelayedexpansion

REM Script para instalar el GLPI Bot como tarea programada de Windows
REM Esto ejecutará el bot automáticamente al iniciar el sistema

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        GLPI BOT 24/7 - Instalación como Servicio           ║
echo ║         Versión 1.0 (Windows Task Scheduler)               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Este script requiere permisos de Administrador
    echo.
    echo Por favor:
    echo 1. Abre PowerShell como Administrador
    echo 2. Ejecuta el comando:
    echo    cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
    echo    powershell -ExecutionPolicy Bypass -File install_bot_service.ps1
    echo.
    pause
    exit /b 1
)

echo ✅ Permisos de administrador detectados
echo.
echo Instalando tarea programada...

REM Variables
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%run_bot_with_restart.ps1"
set "TASK_NAME=GLPIBot24-7"

REM Crear la tarea programada
schtasks /create /tn "!TASK_NAME!" /tr "powershell.exe -ExecutionPolicy Bypass -File \"!SCRIPT_PATH!\"" /sc onstart /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ ¡Instalación completada con éxito!
    echo.
    echo 📌 Detalles:
    echo    • Nombre de tarea: %TASK_NAME%
    echo    • Ubicación: C:\Windows\System32\Tasks\
    echo    • Ejecución: Al iniciar Windows (con permisos de admin)
    echo    • Script: %SCRIPT_PATH%
    echo.
    echo 🎬 El bot se iniciará automáticamente en el próximo reinicio.
    echo.
    echo Para iniciarlo ahora, ejecuta:
    echo    schtasks /run /tn "%TASK_NAME%"
    echo.
    echo Para ver logs en tiempo real, abre:
    echo    C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent\logs\
    echo.
) else (
    echo.
    echo ❌ Error al crear la tarea programada
    echo.
)

pause
