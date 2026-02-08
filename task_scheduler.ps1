# PowerShell script for running ScriptLauncher via module execution
# Updated for: python -m script_launcher
# Created: 2025-11-22
# Updated: 2025-12-26

# -----------------------------
# Configuration
# -----------------------------

# Python executable
$pythonPath = "C:\Users\james\AppData\Local\Programs\Python\Python310\python.exe"

# Project root (IMPORTANT: this must be py_scripts)
$projectRoot = "C:\Users\james\projects\py_scripts"

# Log directory and file
$logDir = "$projectRoot\logs"
$logFile = "$logDir\script_launcher.log"

# -----------------------------
# Setup
# -----------------------------

# Ensure log directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Change to project root
Set-Location $projectRoot

# Log start
$startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "`n[$startTime] Starting ScriptLauncher"

# -----------------------------
# Execution
# -----------------------------

try {
    # Run ScriptLauncher as a module
    $output = & $pythonPath -m script_launcher 2>&1

    # Log output
    $output | Add-Content -Path $logFile

    if ($LASTEXITCODE -eq 0) {
        $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $logFile -Value "[$endTime] ScriptLauncher exited successfully"
        exit 0
    }
    else {
        $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $logFile -Value "[$endTime] ScriptLauncher failed with exit code $LASTEXITCODE"
        exit $LASTEXITCODE
    }
}
catch {
    $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $errorMsg = "[$endTime] ScriptLauncher crashed: $($_.Exception.Message)"
    Add-Content -Path $logFile -Value $errorMsg
    exit 1
}
