#!/bin/bash

echo "========================================"
echo "   Mario Maze Race - Linux Launcher"
echo "========================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed!"
    echo "Install with: sudo apt install python3 python3-pip"
    exit 1
fi

python3 --version

# Check Pygame installation
echo ""
echo "Checking Pygame installation..."
if ! python3 -c "import pygame" &> /dev/null
then
    echo "Pygame not found. Installing..."
    pip3 install --user pygame
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Pygame!"
        echo "Try: sudo apt install python3-pygame"
        exit 1
    fi
fi

echo ""
echo "Starting Mario Maze Race..."
echo ""
echo "Controls:"
echo "  Arrow Keys - Move Mario"
echo "  R - Restart game (when game over)"
echo "  Q - Quit game (when game over)"
echo ""
echo "Good luck beating Luigi!"
echo ""

python3 mario_maze.py
