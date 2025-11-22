@echo off
REM Batch file for running Python script with Task Scheduler
REM Created: 2025-11-22

REM Set the path to your Python executable
SET PYTHON_PATH=C:\Users\james\AppData\Local\Programs\Python\Python310\python.exe

REM Set the path to your Python script
SET SCRIPT_PATH=C:\Users\james\projects\py_scripts\script_launcher.py

REM Optional: Set the working directory (where the script should run from)
CD /D "C:\Users\james\projects\py_scripts"

REM Optional: Activate virtual environment if you're using one
REM CALL C:\path\to\venv\Scripts\activate.bat

REM Set log file path
SET LOG_FILE=C:\Users\james\projects\py_scripts\logs\execution_log.txt

REM Run the Python script and log output
echo Running Python script at %date% %time% >> "%LOG_FILE%"
"%PYTHON_PATH%" "%SCRIPT_PATH%" >> "%LOG_FILE%" 2>&1

REM Check if script ran successfully
IF %ERRORLEVEL% EQU 0 (
    echo Script completed successfully at %date% %time% >> execution_log.txt
) ELSE (
    echo Script failed with error code %ERRORLEVEL% at %date% %time% >> execution_log.txt
)

REM Optional: Pause to see output (remove this for scheduled tasks)
REM pause

exit /b %ERRORLEVEL%