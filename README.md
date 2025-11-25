# mind_games


# Mario Maze Game - Multi-Platform

A Mario-themed maze game where you compete against an AI to solve the maze first!

## 🎮 Game Features

- **Player vs AI Competition**: Race against an intelligent AI opponent
- **Mario Theme**: Classic Mario-style graphics and colors
- **Dynamic Maze Generation**: Each game creates a unique maze
- **Multi-Platform Support**: Windows, Linux, Web, and Android versions

## 📁 Project Structure

```
ml_game/
├── windows/          # Windows desktop version (Python/Pygame)
├── linux/            # Linux desktop version (Python/Pygame)
├── web/              # Web browser version (HTML5/JavaScript)
├── android/          # Android app version
├── assets/           # Shared game assets and resources
└── README.md         # This file
```

## 🚀 Quick Start

### Windows
```bash
cd windows
pip install -r requirements.txt
python mario_maze.py
```

### Linux
```bash
cd linux
pip3 install -r requirements.txt
python3 mario_maze.py
```

### Web
```bash
cd web
# Open index.html in your browser or serve with:
python -m http.server 8000
# Then navigate to http://localhost:8000
```

### Android
```bash
cd android
# Follow instructions in android/README.md
```

## 🎯 How to Play

1. **Objective**: Reach the green goal before the AI does!
2. **Controls**:
   - Desktop: Arrow keys to move
   - Web: Arrow keys or WASD
   - Android: Touch controls
3. **Rules**: Navigate through the maze, avoid walls, and beat the AI!

## 🏗️ Technology Stack

- **Desktop (Windows/Linux)**: Python 3.7+, Pygame
- **Web**: HTML5, CSS3, JavaScript (Canvas API)
- **Android**: WebView wrapper with Cordova

## 📝 License

MIT License - Feel free to use and modify!

## 🎨 Credits

Created with ❤️ for Mario fans everywhere!
