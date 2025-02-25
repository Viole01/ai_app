@echo off
:: Define variables
set "REMOTE_USER=ubuntu"
set "REMOTE_HOST=your-remote-server"
set "REMOTE_DIR=/home/ubuntu/ai_app"
set "SERVICE_NAME=fastapi.service"
set "PRIVATE_KEY=C:\path\to\private_key.pem"

:: Construct the SSH command
set "REMOTE_COMMAND=cd %REMOTE_DIR% && git pull && sudo systemctl restart %SERVICE_NAME%"

:: Execute the SSH command
ssh -i "%PRIVATE_KEY%" "%REMOTE_USER%@%REMOTE_HOST%" "%REMOTE_COMMAND%"

:: Check exit status
if %errorlevel% equ 0 (
    echo Commands executed successfully on %REMOTE_HOST%.
) else (
    echo Error occurred while executing commands on %REMOTE_HOST%.
    pause
)

:: Pause at the end to keep the console open
pause
