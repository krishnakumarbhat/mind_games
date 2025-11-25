# Mario Maze Game - Web Version

## Overview

A browser-based Mario-themed maze game built with HTML5 Canvas and JavaScript. Race against Luigi (AI) to solve the maze!

## Features

- Pure HTML5/CSS3/JavaScript - no dependencies
- Responsive design
- Works on all modern browsers
- Touch-friendly controls
- Dynamic maze generation
- Smart AI with A* pathfinding

## Running the Game

### Option 1: Direct File Open
Simply open `index.html` in your web browser.

### Option 2: Local Server (Recommended)

#### Using Python 3:
```bash
python -m http.server 8000
```

#### Using Python 2:
```bash
python -m SimpleHTTPServer 8000
```

#### Using Node.js:
```bash
npx http-server -p 8000
```

Then navigate to: `http://localhost:8000`

## Controls

- **Arrow Keys** or **WASD**: Move Mario
- **New Maze Button**: Generate a new maze
- **Restart Button**: Restart after game over

## Game Objective

Navigate Mario (red) through the maze to reach the green goal before Luigi (green AI opponent) does!

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+
- Opera 47+

## File Structure

```
web/
├── index.html      # Main HTML file
├── styles.css      # Styling and layout
├── maze.js         # Maze generation and pathfinding
├── game.js         # Main game logic
└── README.md       # This file
```

## Technologies Used

- **HTML5 Canvas**: For game rendering
- **CSS3**: For styling and animations
- **JavaScript ES6**: For game logic
- **A* Algorithm**: For AI pathfinding
- **Depth-First Search**: For maze generation

## Hosting

You can easily host this game on:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

Simply upload all files in the web folder.

## Performance

- Optimized rendering
- Smooth 60 FPS gameplay
- Low CPU usage
- Works on mobile devices

## License

MIT License - Free to use and modify!
