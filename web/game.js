// Main game logic

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const CELL_SIZE = 30;
const MAZE_COLS = 20;
const MAZE_ROWS = 15;
const CANVAS_WIDTH = MAZE_COLS * CELL_SIZE;
const CANVAS_HEIGHT = MAZE_ROWS * CELL_SIZE;

canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

// Colors
const COLORS = {
    wall: '#8B4513',
    path: '#FFFFFF',
    pathBorder: '#CCCCCC',
    goal: '#22B14C',
    mario: '#DC143C',
    luigi: '#22B14C',
    white: '#FFFFFF',
    black: '#000000',
    background: '#87CEEB'
};

class Player {
    constructor(maze, x, y, color) {
        this.x = x;
        this.y = y;
        this.maze = maze;
        this.color = color;
    }

    move(dx, dy) {
        const newX = this.x + dx;
        const newY = this.y + dy;

        if (newX >= 0 && newX < MAZE_COLS &&
            newY >= 0 && newY < MAZE_ROWS &&
            this.maze[newY][newX] === 0) {
            this.x = newX;
            this.y = newY;
            return true;
        }
        return false;
    }

    draw() {
        const x = this.x * CELL_SIZE;
        const y = this.y * CELL_SIZE;
        const centerX = x + CELL_SIZE / 2;
        const centerY = y + CELL_SIZE / 2;

        // Body (circle)
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(centerX, centerY, CELL_SIZE / 3, 0, Math.PI * 2);
        ctx.fill();

        // Hat
        ctx.fillStyle = this.color;
        ctx.fillRect(x + 5, y + 5, CELL_SIZE - 10, 8);

        // Eyes
        ctx.fillStyle = COLORS.white;
        ctx.beginPath();
        ctx.arc(x + 12, y + 15, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + 18, y + 15, 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = COLORS.black;
        ctx.beginPath();
        ctx.arc(x + 12, y + 15, 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + 18, y + 15, 2, 0, Math.PI * 2);
        ctx.fill();

        // Mustache (only for Mario)
        if (this.color === COLORS.mario) {
            ctx.strokeStyle = COLORS.black;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(x + 10, y + 20);
            ctx.lineTo(x + 20, y + 20);
            ctx.stroke();
        }
    }
}

class AIPlayer extends Player {
    constructor(maze, x, y, goalX, goalY) {
        super(maze, x, y, COLORS.luigi);
        this.goalX = goalX;
        this.goalY = goalY;
        this.path = [];
        this.moveDelay = 0;
        this.moveSpeed = 8; // Move every 8 frames
        this.pathFinder = new PathFinder(maze);
    }

    update() {
        this.moveDelay++;

        if (this.moveDelay >= this.moveSpeed) {
            this.moveDelay = 0;

            if (this.path.length === 0) {
                this.path = this.pathFinder.findPath([this.x, this.y], [this.goalX, this.goalY]);
            }

            if (this.path.length > 0) {
                const [nextX, nextY] = this.path.shift();
                this.x = nextX;
                this.y = nextY;
            }
        }
    }
}

class Game {
    constructor() {
        this.maze = null;
        this.player = null;
        this.ai = null;
        this.goalX = MAZE_COLS - 1;
        this.goalY = MAZE_ROWS - 1;
        this.gameOver = false;
        this.winner = null;
        this.animationId = null;

        this.setupControls();
        this.newGame();
    }

    newGame() {
        // Generate maze
        const generator = new MazeGenerator(MAZE_COLS, MAZE_ROWS);
        this.maze = generator.generate();

        // Initialize players
        this.player = new Player(this.maze, 0, 0, COLORS.mario);
        this.ai = new AIPlayer(this.maze, 0, 0, this.goalX, this.goalY);

        // Reset game state
        this.gameOver = false;
        this.winner = null;

        // Hide game over screen
        document.getElementById('gameOver').classList.add('hidden');

        // Start game loop
        if (!this.animationId) {
            this.gameLoop();
        }
    }

    setupControls() {
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (this.gameOver) return;

            switch (e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    this.player.move(0, -1);
                    e.preventDefault();
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    this.player.move(0, 1);
                    e.preventDefault();
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    this.player.move(-1, 0);
                    e.preventDefault();
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    this.player.move(1, 0);
                    e.preventDefault();
                    break;
            }
        });

        // Button controls
        document.getElementById('newMazeBtn').addEventListener('click', () => {
            this.newGame();
        });

        document.getElementById('restartBtn').addEventListener('click', () => {
            this.newGame();
        });
    }

    checkWinner() {
        if (this.player.x === this.goalX && this.player.y === this.goalY) {
            this.gameOver = true;
            this.winner = 'Mario';
            this.showGameOver();
        } else if (this.ai.x === this.goalX && this.ai.y === this.goalY) {
            this.gameOver = true;
            this.winner = 'Luigi';
            this.showGameOver();
        }
    }

    showGameOver() {
        const gameOverDiv = document.getElementById('gameOver');
        const winnerText = document.getElementById('winnerText');

        if (this.winner === 'Mario') {
            winnerText.textContent = 'YOU WIN! 🎉';
            winnerText.style.color = COLORS.mario;
        } else {
            winnerText.textContent = 'LUIGI WINS! 😅';
            winnerText.style.color = COLORS.luigi;
        }

        gameOverDiv.classList.remove('hidden');
    }

    drawMaze() {
        for (let y = 0; y < MAZE_ROWS; y++) {
            for (let x = 0; x < MAZE_COLS; x++) {
                const px = x * CELL_SIZE;
                const py = y * CELL_SIZE;

                if (this.maze[y][x] === 1) {
                    // Wall
                    ctx.fillStyle = COLORS.wall;
                    ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
                    ctx.strokeStyle = COLORS.black;
                    ctx.lineWidth = 1;
                    ctx.strokeRect(px, py, CELL_SIZE, CELL_SIZE);
                } else {
                    // Path
                    ctx.fillStyle = COLORS.path;
                    ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
                    ctx.strokeStyle = COLORS.pathBorder;
                    ctx.lineWidth = 1;
                    ctx.strokeRect(px, py, CELL_SIZE, CELL_SIZE);
                }
            }
        }

        // Draw goal
        const goalX = this.goalX * CELL_SIZE;
        const goalY = this.goalY * CELL_SIZE;
        ctx.fillStyle = COLORS.goal;
        ctx.fillRect(goalX, goalY, CELL_SIZE, CELL_SIZE);
        ctx.strokeStyle = COLORS.black;
        ctx.lineWidth = 2;
        ctx.strokeRect(goalX, goalY, CELL_SIZE, CELL_SIZE);

        // Draw "GOAL" text
        ctx.fillStyle = COLORS.white;
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('GOAL', goalX + CELL_SIZE / 2, goalY + CELL_SIZE / 2);
    }

    update() {
        if (!this.gameOver) {
            this.ai.update();
            this.checkWinner();
        }
    }

    draw() {
        // Clear canvas
        ctx.fillStyle = COLORS.background;
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

        // Draw game elements
        this.drawMaze();
        this.player.draw();
        this.ai.draw();
    }

    gameLoop() {
        this.update();
        this.draw();
        this.animationId = requestAnimationFrame(() => this.gameLoop());
    }
}

// Start the game
const game = new Game();
