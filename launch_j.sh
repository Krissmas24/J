#!/bin/bash
# Launcher for J Macro
# Ensures only one instance is running

PROJECT_DIR="/home/krissmas01/j_macro"

# Check if already running
if pgrep -f "python3 $PROJECT_DIR/main.py" > /dev/null; then
    # If using Hyprland, we could focus the window, but for now just exit
    exit 0
fi

# Change to project directory to ensure relative imports work if any
cd "$PROJECT_DIR" || exit

# Run the app using the absolute path to python
/usr/bin/python3 main.py &
