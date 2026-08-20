# Script PowerShell para instalar el GLPI Bot como servicio Windows
# Ejecutar como Administrador

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================================"
Write-Host "  GLPI BOT 24/7 - Installation as Service"
Write-Host "========================================================"
Write-Host ""

# Check for admin rights
$IsAdmin = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains `
    [Security.Principal.SecurityIdentifier]"S-1-5-32-544"

if (-not $IsAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges"
    Write-Host ""
    Write-Host "Please:"
    Write-Host "1. Right-click on PowerShell"
    Write-Host "2. Select 'Run as administrator'"
    Write-Host "3. Run this script again"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK - Administrator privileges detected"
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ScriptDir "run_bot_with_restart.ps1"
$TaskName = "GLPIBot24-7"

Write-Host "Installing scheduled task..."
Write-Host "  Location: $ScriptPath"
Write-Host "  Task Name: $TaskName"
Write-Host ""

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found: $ScriptPath"
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    # Create task action
    $Action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`""

    # Create trigger (at startup)
    $Trigger = New-ScheduledTaskTrigger -AtStartup

    # Create settings
    $Settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -Compatibility Win8 `
        -StartWhenAvailable

    # Create the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host ""
    Write-Host "SUCCESS - Installation completed!"
    Write-Host ""
    Write-Host "Details:"
    Write-Host "  Task Name: $TaskName"
    Write-Host "  Execution: At Windows startup (with admin rights)"
    Write-Host "  Auto-restart: Enabled (if bot fails)"
    Write-Host "  Logs: $ScriptDir\logs\bot_restart.log"
    Write-Host ""
    Write-Host "To start the bot now, run:"
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    Write-Host "To monitor logs in real-time:"
    Write-Host "  Get-Content '$ScriptDir\logs\bot_restart.log' -Wait -Tail 20"
    Write-Host ""
    Write-Host "To manage the task:"
    Write-Host "  Open: Task Scheduler (taskschd.msc)"
    Write-Host "  Find: $TaskName"
    Write-Host "  Right-click: Properties, Run, Disable, Delete, etc."
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "ERROR creating task:"
    Write-Host "  $_"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to close"
