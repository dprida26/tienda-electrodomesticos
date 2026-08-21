# Script para ejecutar el bot 24/7 con auto-reinicio
# Este script mantiene el bot corriendo incluso si falla

$BotPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $BotPath "logs\bot_restart.log"
$MaxFailures = 5
$FailureResetTime = 300  # 5 minutos
$RestartDelay = 5  # 5 segundos entre intentos

# Crear carpeta de logs si no existe
$LogDir = Join-Path $BotPath "logs"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }

function Log-Message {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMsg = "$Timestamp │ $Message"
    Add-Content $LogFile $LogMsg
    Write-Host $LogMsg
}

Log-Message "╔════════════════════════════════════════╗"
Log-Message "║  🤖 GLPI Bot 24/7 - Auto Restart      ║"
Log-Message "║  Versión: 1.0 (PowerShell)            ║"
Log-Message "╚════════════════════════════════════════╝"
Log-Message ""
Log-Message "📍 Ubicación: $BotPath"
Log-Message "📝 Logs: $LogFile"
Log-Message "⏱️  Reinicio automático: Habilitado"
Log-Message "🔄 Intentos máximos antes de alertar: $MaxFailures"
Log-Message ""
Log-Message "Iniciando monitoreo..."

$FailureCount = 0
$LastResetTime = Get-Date

while ($true) {
    try {
        Log-Message "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        Log-Message "▶️  Iniciando bot... (Intento $($FailureCount + 1)/$MaxFailures)"
        Log-Message "📅 $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        Log-Message ""

        # Ejecutar el bot
        $Process = Start-Process -FilePath "python" `
            -ArgumentList "$BotPath\bot_24_7.py" `
            -NoNewWindow `
            -Wait `
            -PassThru

        $ExitCode = $Process.ExitCode
        Log-Message "⛔ Bot finalizado con código: $ExitCode"

        # Si el bot se ejecutó correctamente (exit code 0), resetear contador de fallos
        if ($ExitCode -eq 0) {
            Log-Message "✅ Ejecución completada exitosamente"
            $FailureCount = 0
            Log-Message "🔄 Reiniciando en $RestartDelay segundos..."
        } else {
            # Increment failure counter
            $FailureCount++

            # Chequear si es tiempo de resetear el contador
            $Now = Get-Date
            if (($Now - $LastResetTime).TotalSeconds -gt $FailureResetTime) {
                Log-Message "✅ Período de gracia transcurrido, reseteando contador de fallos"
                $FailureCount = 1
                $LastResetTime = $Now
            }

            if ($FailureCount -ge $MaxFailures) {
                Log-Message ""
                Log-Message "❌ ¡ERROR CRÍTICO! El bot ha fallado $MaxFailures veces consecutivas"
                Log-Message "❌ Últimas 5 líneas del error:"
                Log-Message ""
                Log-Message "⏰ Esperando 60 segundos antes de reintentar..."
                Start-Sleep -Seconds 60
                $FailureCount = 0
                $LastResetTime = Get-Date
                Log-Message "🔄 Reintentando..."
            } else {
                Log-Message "⚠️  Fallo #$FailureCount de $MaxFailures"
                Log-Message "🔄 Reiniciando en $RestartDelay segundos..."
            }
        }

        Start-Sleep -Seconds $RestartDelay

    } catch {
        $FailureCount++
        Log-Message "❌ Excepción: $_"

        if ($FailureCount -ge $MaxFailures) {
            Log-Message "❌ Límite de intentos alcanzado"
            Start-Sleep -Seconds 60
            $FailureCount = 0
        }

        Log-Message "🔄 Reintentando en $RestartDelay segundos..."
        Start-Sleep -Seconds $RestartDelay
    }
}
