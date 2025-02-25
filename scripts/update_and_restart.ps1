# Define variables
$RemoteUser = "ubuntu"                  # Remote server username
$RemoteHost = "your-remote-server"      # Remote server address (IP or hostname)
$RemoteDir = "/home/ubuntu/ai_app"      # Directory on the remote server
$ServiceName = "fastapi.service"        # Service to restart
$PrivateKeyPath = "C:\path\to\private_key.pem"  # Path to your private key file

# Command to execute on the remote server
$RemoteCommand = @"
cd $RemoteDir
git pull
sudo systemctl restart $ServiceName
"@

# Execute SSH command
try {
    ssh -i $PrivateKeyPath "$RemoteUser@$RemoteHost" $RemoteCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Commands executed successfully on $RemoteHost."
    } else {
        Write-Error "Error occurred while executing commands on $RemoteHost."
    }
} catch {
    Write-Error "Failed to connect to $RemoteHost: $_"
}

# For debugging use this command
# ssh -v -i $PrivateKeyPath "$RemoteUser@$RemoteHost" $RemoteCommand
