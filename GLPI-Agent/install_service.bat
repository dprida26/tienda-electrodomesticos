@echo off
echo ============================================
echo   GLPI Agent - Instalador de Servicio
echo ============================================
echo.

:: Obtener ruta del script
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=python
set MAIN_SCRIPT=%SCRIPT_DIR%main.py

echo Registrando tarea programada en Windows...
echo Ruta: %MAIN_SCRIPT%
echo.

:: Crear tarea programada que se ejecute al iniciar sesión
schtasks /create /tn "GLPI_Agent_Bot" /tr "cmd /c %PYTHON_PATH% \"%MAIN_SCRIPT%\"" /sc ONLOGON /rl HIGHEST /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ Tarea programada creada exitosamente.
    echo    El agente se iniciará automáticamente al encender la PC.
    echo.
    echo    Para iniciar ahora: python main.py
    echo    Para eliminar: schtasks /delete /tn "GLPI_Agent_Bot" /f
) else (
    echo.
    echo ❌ Error al crear la tarea. Ejecuta este script como Administrador.
)
echo.
pause
