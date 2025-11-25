#!/bin/bash

echo "========================================"
echo "  Mario Maze Race - Web Server Launcher"
echo "========================================"
echo ""
echo "Starting local web server..."
echo ""
echo "The game will be available at:"
echo "  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Try Python 3 first, then Python 2
if command -v python3 &> /dev/null
then
    python3 -m http.server 8000
elif command -v python &> /dev/null
then
    python -m SimpleHTTPServer 8000
else
    echo "ERROR: Python is not installed!"
    exit 1
fi
