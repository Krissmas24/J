#!/bin/bash
# Launcher for J Macro
# Ensures only one instance is running

PROJECT_DIR="/home/krissmas01/j_macro"
LOG_FILE="/home/krissmas01/.fisch_macro/launcher.log"

mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date)] Launching J Macro..." >> "$LOG_FILE"

# Check if already running
PID=$(pgrep -f "python3 $PROJECT_DIR/main.py")
if [ -n "$PID" ]; then
    echo "[$(date)] Already running with PID $PID. Exiting." >> "$LOG_FILE"
    exit 0
fi

# Change to project directory
cd "$PROJECT_DIR" || { echo "[$(date)] Failed to cd to $PROJECT_DIR" >> "$LOG_FILE"; exit 1; }

# Run the app
/usr/bin/python3 main.py >> "$LOG_FILE" 2>&1 &
echo "[$(date)] J Macro started in background." >> "$LOG_FILE"
