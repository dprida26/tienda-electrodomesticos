# GLPI Agent - Inicia Scheduler y Bot Interactivo
$env:PYTHONIOENCODING = 'utf-8'
$projectPath = "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
cd $projectPath

Write-Host "======================================"
Write-Host "GLPI AGENT - Iniciando servicios"
Write-Host "======================================"
Write-Host ""

# Iniciar Scheduler en background
Write-Host "[1/2] Iniciando Scheduler (Reportes automáticos)..."
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden -WorkingDirectory $projectPath

# Esperar 2 segundos
Start-Sleep -Seconds 2

# Iniciar Bot Interactivo en background
Write-Host "[2/2] Iniciando Bot Interactivo (Bajo demanda)..."
Start-Process python -ArgumentList "telegram_bot_interactive.py" -WindowStyle Hidden -WorkingDirectory $projectPath

Write-Host ""
Write-Host "✅ Ambos servicios iniciados!"
Write-Host ""
Write-Host "Estado:"
Write-Host "  - Scheduler: Reportes a las 08:00 y 17:00"
Write-Host "  - Bot: Escucha comandos /reporte en Telegram"
Write-Host ""
Write-Host "Presiona Ctrl+C para detener"

# Mantener el script corriendo
while ($true) {
    Start-Sleep -Seconds 60

    # Verificar si los procesos siguen corriendo
    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue
    if ($null -eq $pythonProcs) {
        Write-Host "Procesos detenidos. Reintentando en 10 segundos..."
        Start-Sleep -Seconds 10
        Start-Process python -ArgumentList "main.py" -WindowStyle Hidden -WorkingDirectory $projectPath
        Start-Sleep -Seconds 2
        Start-Process python -ArgumentList "telegram_bot_interactive.py" -WindowStyle Hidden -WorkingDirectory $projectPath
    }
}
