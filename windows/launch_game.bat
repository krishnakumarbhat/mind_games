@echo off
echo ========================================
echo    Mario Maze Race - Windows Launcher
echo ========================================
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Checking Pygame installation...
pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame not found. Installing...
    pip install pygame
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Pygame!
        pause
        exit /b 1
    )
)

echo.
echo Starting Mario Maze Race...
echo.
echo Controls:
echo   Arrow Keys - Move Mario
echo   R - Restart game (when game over)
echo   Q - Quit game (when game over)
echo.
echo Good luck beating Luigi!
echo.
python mario_maze.py
pause
