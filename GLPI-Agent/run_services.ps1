# GLPI Agent - Ejecuta y mantiene vivos los servicios
param(
    [string]$Mode = "both"
)

$env:PYTHONIOENCODING = 'utf-8'
$projectPath = "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
cd $projectPath

function Start-Service {
    param(
        [string]$Script,
        [string]$Name
    )

    $process = Start-Process python -ArgumentList $Script -PassThru -NoNewWindow
    Write-Host "✅ $Name iniciado (PID: $($process.Id))"
    return $process
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "GLPI AGENT - Servicios en Ejecución" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

$processes = @()

if ($Mode -eq "both" -or $Mode -eq "scheduler") {
    $p1 = Start-Service "main.py" "Scheduler (Reportes automáticos)"
    $processes += $p1
    Start-Sleep -Seconds 1
}

if ($Mode -eq "both" -or $Mode -eq "bot") {
    $p2 = Start-Service "telegram_bot_interactive.py" "Bot Interactivo"
    $processes += $p2
}

Write-Host ""
Write-Host "Estado actual:" -ForegroundColor Cyan
Write-Host "  📅 Scheduler: Reportes a las 08:00 y 17:00"
Write-Host "  🤖 Bot: Escuchando comandos /reporte"
Write-Host ""
Write-Host "Procesos en ejecución: $($processes.Count)" -ForegroundColor Yellow
Write-Host ""

# Mantener vivo el script y reiniciar si algo falla
$lastCheck = Get-Date
while ($true) {
    Start-Sleep -Seconds 30

    foreach ($process in $processes) {
        if ($process.HasExited) {
            Write-Host "⚠️  Proceso $($process.Id) terminado. Reintentando..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5

            # Reiniciar
            if ($process.Name -like "*main*") {
                $newProc = Start-Service "main.py" "Scheduler"
            } else {
                $newProc = Start-Service "telegram_bot_interactive.py" "Bot Interactivo"
            }
            $processes[$processes.IndexOf($process)] = $newProc
        }
    }

    # Log de estado cada 5 minutos
    $now = Get-Date
    if (($now - $lastCheck).TotalSeconds -ge 300) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Servicios activos: $($processes.Count)" -ForegroundColor DarkGray
        $lastCheck = $now
    }
}
