# Mario Maze Game - Linux Version

## Requirements

- Python 3.7 or higher
- Pygame library
- SDL development libraries (for Pygame)

## Installation

### Ubuntu/Debian

1. Install Python and dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-dev
   sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Fedora/RHEL

1. Install Python and dependencies:
   ```bash
   sudo dnf install python3 python3-pip python3-devel
   sudo dnf install SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

### Arch Linux

1. Install Python and dependencies:
   ```bash
   sudo pacman -S python python-pip
   sudo pacman -S sdl2 sdl2_image sdl2_mixer sdl2_ttf
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the Game

```bash
python3 mario_maze.py
```

Or make it executable:
```bash
chmod +x mario_maze.py
./mario_maze.py
```

## Controls

- **Arrow Keys**: Move Mario through the maze
- **R**: Restart game (when game is over)
- **Q**: Quit game (when game is over)

## Objective

Race against Luigi (AI) to reach the green goal at the bottom-right corner of the maze!

## Features

- Dynamic maze generation - each game is unique
- Smart AI opponent using A* pathfinding
- Mario-themed graphics and colors
- Smooth gameplay at 60 FPS

## Troubleshooting

**Issue**: "No module named 'pygame'"
**Solution**: Run `pip3 install --user pygame`

**Issue**: "SDL not found" errors
**Solution**: Install SDL development libraries for your distribution (see Installation section)

**Issue**: Display issues
**Solution**: Make sure you have a display server running (X11 or Wayland)

## System Requirements

- Linux kernel 3.x or higher
- X11 or Wayland display server
- 100 MB free disk space
- Any modern CPU
