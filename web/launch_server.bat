@echo off
echo ========================================
echo   Mario Maze Race - Web Server Launcher
echo ========================================
echo.
echo Starting local web server...
echo.
echo The game will be available at:
echo   http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
start http://localhost:8000
python -m http.server 8000
