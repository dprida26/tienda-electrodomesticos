# Script simple para ejecutar el bot GLPI 24/7 con reinicio automático
# Sin caracteres especiales para evitar problemas de encoding

$BotPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$BotScript = Join-Path $BotPath "bot_24_7.py"
$LogDir = Join-Path $BotPath "logs"

# Crear carpeta de logs
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
}

$LogFile = Join-Path $LogDir "bot_restart.log"

function Log-Message {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMsg = "$Timestamp | $Message"
    Add-Content $LogFile $LogMsg
    Write-Host $LogMsg
}

Log-Message "========================================"
Log-Message "GLPI Bot 24/7 - Auto Restart"
Log-Message "========================================"
Log-Message "Location: $BotPath"
Log-Message "Script: $BotScript"
Log-Message "Logs: $LogFile"
Log-Message ""

$FailureCount = 0
$MaxFailures = 5
$RestartDelay = 5

while ($true) {
    try {
        Log-Message "========================================"
        Log-Message "Starting bot... (Attempt $($FailureCount + 1)/$MaxFailures)"
        Log-Message "Time: $(Get-Date)"
        Log-Message ""

        # Execute bot
        $Process = Start-Process -FilePath "python" `
            -ArgumentList "$BotScript" `
            -NoNewWindow `
            -Wait `
            -PassThru

        $ExitCode = $Process.ExitCode
        Log-Message "Bot exited with code: $ExitCode"

        # Reset failure count on success
        if ($ExitCode -eq 0) {
            Log-Message "SUCCESS - Bot completed normally"
            $FailureCount = 0
        } else {
            # Increment failures
            $FailureCount++

            if ($FailureCount -ge $MaxFailures) {
                Log-Message "CRITICAL - Bot failed $MaxFailures times in a row"
                Log-Message "Waiting 60 seconds before retry..."
                Start-Sleep -Seconds 60
                $FailureCount = 0
                Log-Message "Retrying..."
            } else {
                Log-Message "WARNING - Failure #$FailureCount of $MaxFailures"
            }
        }

        Log-Message "Restarting in $RestartDelay seconds..."
        Start-Sleep -Seconds $RestartDelay

    } catch {
        $FailureCount++
        Log-Message "ERROR - Exception: $_"

        if ($FailureCount -ge $MaxFailures) {
            Log-Message "CRITICAL - Reached max failures"
            Start-Sleep -Seconds 60
            $FailureCount = 0
        }

        Log-Message "Retrying in $RestartDelay seconds..."
        Start-Sleep -Seconds $RestartDelay
    }
}
