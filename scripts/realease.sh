#!/bin/bash

# Define variables
REMOTE_USER="ubuntu"
REMOTE_HOST="remote_host"
REMOTE_DIR="/home/ubuntu/ai_app"
SERVICE_NAME="fastapi_service"
SSH_KEY="path_to_key"

# Run commands on the remote server
ssh -i "${SSH_KEY}" "${REMOTE_USER}@${REMOTE_HOST}" << EOF
  cd "${REMOTE_DIR}" || exit 1
  git pull || exit 1
  sudo systemctl restart "${SERVICE_NAME}" || exit 1
EOF

# Check exit status
if [ $? -eq 0 ]; then
  echo "Commands executed successfully on ${REMOTE_HOST}."
else
  echo "Error occurred while executing commands on ${REMOTE_HOST}."
fi
