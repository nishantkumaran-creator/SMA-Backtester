#!/bin/bash

echo "Starting SMA Backtester..."

# 1. Check if Docker is actually running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please open Docker Desktop and try again."
  exit 1
fi

# 2. Try to start an existing container, OR run a new one if it doesn't exist
# We use '2>/dev/null' to hide the error message if the container doesn't exist yet
if [ ! "$(docker ps -q -f name=backtester_app)" ]; then
    if [ "$(docker ps -aq -f name=backtester_app)" ]; then
        echo "Waking up existing container..."
        docker start backtester_app
    else
        echo "🆕 Creating new container..."
        docker run -d -p 8501:8501 --name backtester_app SMA-backtester
    fi
else
    echo "App is already running!"
fi

# 3. Wait a moment for the server to spin up
echo "Waiting for server..."
sleep 3

# 4. Open the Browser (Cross-Platform Logic)
URL="http://localhost:8501"
echo "App is ready at $URL"

# Try Mac command (open), then Linux command (xdg-open), then give up and print url
if [[ "$OSTYPE" == "darwin"* ]]; then
    open $URL
elif command -v xdg-open > /dev/null; then
    xdg-open $URL
else
    echo "Please open your browser to: $URL"
fi