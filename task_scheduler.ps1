# PowerShell script for running Python script with Task Scheduler
# Created: 2025-11-22

# Set the path to your Python executable
$pythonPath = "C:\Users\james\AppData\Local\Programs\Python\Python310\python.exe"

# Set the path to your Python script
$scriptPath = "C:\Users\james\projects\py_scripts\script_launcher.py"

# Set the working directory (where the script should run from)
$workDir = "C:\Users\james\projects\py_scripts"

# Set log file path
$logFile = "C:\Users\james\projects\py_scripts\logs\execution_log.txt"

# Optional: Activate virtual environment if you're using one
# & "C:\path\to\venv\Scripts\Activate.ps1"

# Create logs directory if it doesn't exist
if (-not (Test-Path "C:\logs")) {
    New-Item -ItemType Directory -Path "C:\logs" -Force | Out-Null
}

# Change to working directory
Set-Location $workDir

# Log start time
$startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "`nRunning Python script at $startTime"

try {
    # Run the Python script and capture output
    $output = & $pythonPath $scriptPath 2>&1
    
    # Log the output
    $output | Add-Content -Path $logFile
    
    # Check exit code
    if ($LASTEXITCODE -eq 0) {
        $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $logFile -Value "Script completed successfully at $endTime"
        Write-Host "Script completed successfully" -ForegroundColor Green
        exit 0
    }
    else {
        $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $logFile -Value "Script failed with error code $LASTEXITCODE at $endTime"
        Write-Host "Script failed with error code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}
catch {
    $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $errorMsg = "Script execution failed with exception: $($_.Exception.Message)"
    Add-Content -Path $logFile -Value "$errorMsg at $endTime"
    Write-Host $errorMsg -ForegroundColor Red
    exit 1
}