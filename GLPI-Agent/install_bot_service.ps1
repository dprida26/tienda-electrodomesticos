# Script PowerShell para instalar el GLPI Bot como servicio Windows
# Ejecutar como Administrador

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗"
Write-Host "║        GLPI BOT 24/7 - Instalación como Servicio           ║"
Write-Host "║         Versión 1.0 (Windows Task Scheduler)               ║"
Write-Host "╚════════════════════════════════════════════════════════════╝"
Write-Host ""

# Verificar permisos de administrador
$IsAdmin = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains `
    [Security.Principal.SecurityIdentifier]"S-1-5-32-544"

if (-not $IsAdmin) {
    Write-Host "❌ ERROR: Este script requiere permisos de Administrador"
    Write-Host ""
    Write-Host "Por favor:"
    Write-Host "1. Haz click derecho en PowerShell"
    Write-Host "2. Selecciona 'Ejecutar como administrador'"
    Write-Host "3. Ejecuta nuevamente este script"
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✅ Permisos de administrador detectados"
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ScriptDir "run_bot_with_restart.ps1"
$TaskName = "GLPIBot24-7"

Write-Host "Instalando tarea programada..."
Write-Host "  📍 Script: $ScriptPath"
Write-Host "  📌 Nombre de tarea: $TaskName"
Write-Host ""

# Verificar que el script existe
if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ ERROR: No se encontró el script: $ScriptPath"
    Read-Host "Presiona Enter para salir"
    exit 1
}

try {
    # Crear la acción de la tarea
    $Action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`""

    # Crear el trigger (al iniciar)
    $Trigger = New-ScheduledTaskTrigger -AtStartup

    # Crear configuración avanzada
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -Compatibility Win8 `
        -StartWhenAvailable `
        -MultipleInstancesPolicy IgnoreNew

    # Crear la tarea
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host ""
    Write-Host "✅ ¡Instalación completada con éxito!"
    Write-Host ""
    Write-Host "📌 Detalles:"
    Write-Host "   • Nombre de tarea: $TaskName"
    Write-Host "   • Ejecución: Al iniciar Windows (con permisos de admin)"
    Write-Host "   • Auto-reinicio: Habilitado (si el bot falla)"
    Write-Host "   • Logs: $ScriptDir\logs\bot_restart.log"
    Write-Host ""
    Write-Host "🎬 Para iniciar el bot ahora, ejecuta:"
    Write-Host "   Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    Write-Host "📖 Para ver logs en tiempo real:"
    Write-Host "   Get-Content '$ScriptDir\logs\bot_restart.log' -Wait -Tail 20"
    Write-Host ""
    Write-Host "⚙️  Para gestionar la tarea:"
    Write-Host "   • Abre: Programador de tareas (taskschd.msc)"
    Write-Host "   • Busca: $TaskName"
    Write-Host "   • Click derecho: Propiedades, Ejecutar, Deshabilitar, etc."
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ Error al crear la tarea:"
    Write-Host "   $_"
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Read-Host "Presiona Enter para cerrar"
