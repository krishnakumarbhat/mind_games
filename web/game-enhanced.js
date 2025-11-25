// Enhanced Multi-Level Mario Maze Game with ML

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
    background: '#87CEEB',
    purple: '#9C27B0',
    orange: '#FF9800'
};

// Level configurations
const LEVELS = [
    { id: 1, name: 'A* Pathfinding', algorithm: 'aStar', speed: 8, color: COLORS.luigi, description: 'Optimal pathfinding', unlocked: true },
    { id: 2, name: 'Dijkstra Algorithm', algorithm: 'dijkstra', speed: 7, color: '#1E88E5', description: 'Uniform cost search', unlocked: false },
    { id: 3, name: 'Breadth-First Search', algorithm: 'bfs', speed: 6, color: '#43A047', description: 'Level-by-level exploration', unlocked: false },
    { id: 4, name: 'Depth-First Search', algorithm: 'dfs', speed: 5, color: '#E53935', description: 'Deep exploration first', unlocked: false },
    { id: 5, name: 'Wall-Following', algorithm: 'wallFollowing', speed: 4, color: '#FB8C00', description: 'Right-hand rule', unlocked: false },
    { id: 6, name: 'Q-Learning (RL)', algorithm: 'reinforcementLearning', speed: 6, color: '#8E24AA', description: 'Reinforcement learning', unlocked: false },
    { id: 7, name: 'Genetic Algorithm', algorithm: 'geneticAlgorithm', speed: 7, color: '#00ACC1', description: 'Evolution-based', unlocked: false },
    { id: 8, name: 'Neural Network', algorithm: 'neuralNetwork', speed: 5, color: '#D81B60', description: 'Deep learning', unlocked: false },
    { id: 9, name: 'Imitation Learning', algorithm: 'imitationLearning', speed: 5, color: '#6A1B9A', description: 'Learns from you!', unlocked: false },
    { id: 10, name: 'Diffusion Policy', algorithm: 'diffusionPolicy', speed: 4, color: '#C2185B', description: 'Advanced ML model', unlocked: false }
];

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

        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(centerX, centerY, CELL_SIZE / 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = this.color;
        ctx.fillRect(x + 5, y + 5, CELL_SIZE - 10, 8);

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

class EnhancedAI extends Player {
    constructor(maze, x, y, goalX, goalY, level) {
        super(maze, x, y, level.color);
        this.goalX = goalX;
        this.goalY = goalY;
        this.level = level;
        this.path = [];
        this.moveDelay = 0;
        this.moveSpeed = level.speed;
        this.aiAlgorithms = new AIAlgorithms(maze);
        this.currentState = null;
    }

    findPath() {
        const start = [this.x, this.y];
        const goal = [this.goalX, this.goalY];

        switch(this.level.algorithm) {
            case 'aStar':
                return this.aiAlgorithms.aStar(start, goal);
            case 'dijkstra':
                return this.aiAlgorithms.dijkstra(start, goal);
            case 'bfs':
                return this.aiAlgorithms.bfs(start, goal);
            case 'dfs':
                return this.aiAlgorithms.dfs(start, goal);
            case 'wallFollowing':
                return this.aiAlgorithms.wallFollowing(start, goal);
            case 'reinforcementLearning':
                return this.aiAlgorithms.reinforcementLearning(start, goal);
            case 'geneticAlgorithm':
                return this.aiAlgorithms.geneticAlgorithm(start, goal);
            case 'neuralNetwork':
                return this.aiAlgorithms.neuralNetwork(start, goal);
            case 'imitationLearning':
                return this.useImitationLearning(start, goal);
            case 'diffusionPolicy':
                return this.useDiffusionPolicy(start, goal);
            default:
                return this.aiAlgorithms.aStar(start, goal);
        }
    }

    useImitationLearning(start, goal) {
        if (!game.mlManager.isModelTrained('imitation')) {
            console.log('Imitation model not trained, using A*');
            return this.aiAlgorithms.aStar(start, goal);
        }

        const path = [];
        let current = [...start];
        const visited = new Set([`${start[0]},${start[1]}`]);
        const maxSteps = MAZE_COLS * MAZE_ROWS;

        for (let step = 0; step < maxSteps; step++) {
            if (current[0] === goal[0] && current[1] === goal[1]) break;

            const state = game.dataCollector.encodeState({
                playerPos: current,
                aiPos: [this.x, this.y],
                mazeSnapshot: this.maze
            });

            const action = game.mlManager.predictAction(state, 'imitation');
            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            const [dx, dy] = directions[action];
            const next = [current[0] + dx, current[1] + dy];
            const nextKey = `${next[0]},${next[1]}`;

            if (this.isValidCell(next) && !visited.has(nextKey)) {
                visited.add(nextKey);
                path.push(next);
                current = next;
            } else {
                break;
            }
        }

        if (path.length === 0 || `${current[0]},${current[1]}` !== `${goal[0]},${goal[1]}`) {
            return this.aiAlgorithms.aStar(start, goal);
        }

        return path;
    }

    useDiffusionPolicy(start, goal) {
        if (!game.mlManager.isModelTrained('diffusion')) {
            console.log('Diffusion model not trained, using A*');
            return this.aiAlgorithms.aStar(start, goal);
        }

        const path = [];
        let current = [...start];
        const visited = new Set([`${start[0]},${start[1]}`]);
        const maxSteps = MAZE_COLS * MAZE_ROWS;

        for (let step = 0; step < maxSteps; step++) {
            if (current[0] === goal[0] && current[1] === goal[1]) break;

            const state = game.dataCollector.encodeState({
                playerPos: current,
                aiPos: [this.x, this.y],
                mazeSnapshot: this.maze
            });

            const action = game.mlManager.predictAction(state, 'diffusion');
            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            const [dx, dy] = directions[action];
            const next = [current[0] + dx, current[1] + dy];
            const nextKey = `${next[0]},${next[1]}`;

            if (this.isValidCell(next) && !visited.has(nextKey)) {
                visited.add(nextKey);
                path.push(next);
                current = next;
            } else {
                break;
            }
        }

        if (path.length === 0 || `${current[0]},${current[1]}` !== `${goal[0]},${goal[1]}`) {
            return this.aiAlgorithms.aStar(start, goal);
        }

        return path;
    }

    isValidCell(pos) {
        return pos[0] >= 0 && pos[0] < MAZE_COLS &&
               pos[1] >= 0 && pos[1] < MAZE_ROWS &&
               this.maze[pos[1]][pos[0]] === 0;
    }

    update() {
        this.moveDelay++;

        if (this.moveDelay >= this.moveSpeed) {
            this.moveDelay = 0;

            if (this.path.length === 0) {
                this.path = this.findPath();
            }

            if (this.path.length > 0) {
                const [nextX, nextY] = this.path.shift();
                this.x = nextX;
                this.y = nextY;
            }
        }
    }
}

class EnhancedGame {
    constructor() {
        this.maze = null;
        this.player = null;
        this.ai = null;
        this.goalX = MAZE_COLS - 1;
        this.goalY = MAZE_ROWS - 1;
        this.gameOver = false;
        this.winner = null;
        this.animationId = null;
        this.currentLevel = 1;
        this.levelsCompleted = new Set();
        this.dataCollector = new GameplayDataCollector();
        this.mlManager = new MLModelManager();
        this.lastMove = null;

        this.setupControls();
        this.loadProgress();
        this.showLevelSelect();
    }

    startLevel(levelId) {
        this.currentLevel = levelId;
        const level = LEVELS.find(l => l.id === levelId);
        
        if (!level || !level.unlocked) {
            alert('This level is locked! Complete previous levels first.');
            return;
        }

        document.getElementById('levelSelect').classList.add('hidden');
        this.newGame(level);
    }

    newGame(level) {
        const generator = new MazeGenerator(MAZE_COLS, MAZE_ROWS);
        this.maze = generator.generate();

        this.player = new Player(this.maze, 0, 0, COLORS.mario);
        this.ai = new EnhancedAI(this.maze, 0, 0, this.goalX, this.goalY, level);

        this.gameOver = false;
        this.winner = null;
        this.lastMove = null;

        document.getElementById('gameOver').classList.add('hidden');
        document.getElementById('currentLevelDisplay').textContent = `Level ${level.id}: ${level.name}`;
        document.getElementById('levelDescription').textContent = level.description;

        this.dataCollector.startSession(level.id, this.maze);

        if (!this.animationId) {
            this.gameLoop();
        }
    }

    setupControls() {
        document.addEventListener('keydown', (e) => {
            if (this.gameOver) return;

            let moved = false;
            let action = '';
            const prevPos = [this.player.x, this.player.y];

            switch (e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    moved = this.player.move(0, -1);
                    action = 'up';
                    e.preventDefault();
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    moved = this.player.move(0, 1);
                    action = 'down';
                    e.preventDefault();
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    moved = this.player.move(-1, 0);
                    action = 'left';
                    e.preventDefault();
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    moved = this.player.move(1, 0);
                    action = 'right';
                    e.preventDefault();
                    break;
            }

            if (moved && action) {
                const newPos = [this.player.x, this.player.y];
                this.dataCollector.recordMove(prevPos, newPos, action);
                this.dataCollector.recordState(
                    [this.player.x, this.player.y],
                    [this.ai.x, this.ai.y],
                    this.maze
                );
            }
        });

        document.getElementById('newMazeBtn').addEventListener('click', () => {
            this.showLevelSelect();
        });

        document.getElementById('restartBtn').addEventListener('click', () => {
            const level = LEVELS.find(l => l.id === this.currentLevel);
            this.newGame(level);
        });

        document.getElementById('trainModelsBtn').addEventListener('click', () => {
            this.trainMLModels();
        });

        document.getElementById('showStatsBtn').addEventListener('click', () => {
            this.showStatistics();
        });

        document.getElementById('backToMenuBtn').addEventListener('click', () => {
            this.showLevelSelect();
        });
    }

    checkWinner() {
        if (this.player.x === this.goalX && this.player.y === this.goalY) {
            this.gameOver = true;
            this.winner = 'Mario';
            this.onGameEnd(true);
        } else if (this.ai.x === this.goalX && this.ai.y === this.goalY) {
            this.gameOver = true;
            this.winner = 'Luigi';
            this.onGameEnd(false);
        }
    }

    onGameEnd(won) {
        const sessionData = this.dataCollector.endSession(won, [this.player.x, this.player.y]);
        
        if (won) {
            this.levelsCompleted.add(this.currentLevel);
            
            // Unlock next level
            if (this.currentLevel < LEVELS.length) {
                LEVELS[this.currentLevel].unlocked = true;
            }
            
            this.saveProgress();
        }

        this.showGameOver(won, sessionData);
    }

    showGameOver(won, sessionData) {
        const gameOverDiv = document.getElementById('gameOver');
        const winnerText = document.getElementById('winnerText');
        const statsDiv = document.getElementById('gameStats');

        if (won) {
            winnerText.textContent = '🎉 YOU WIN! 🎉';
            winnerText.style.color = COLORS.mario;
        } else {
            winnerText.textContent = 'AI WINS! 😅';
            winnerText.style.color = COLORS.luigi;
        }

        if (sessionData) {
            statsDiv.innerHTML = `
                <p>Duration: ${(sessionData.duration / 1000).toFixed(1)}s</p>
                <p>Moves: ${sessionData.moves.length}</p>
                <p>Efficiency: ${(sessionData.efficiency * 100).toFixed(1)}%</p>
            `;
        }

        gameOverDiv.classList.remove('hidden');
    }

    async trainMLModels() {
        const stats = this.dataCollector.getStatistics();
        
        if (stats.completedSessions < 5) {
            alert('Play at least 5 games to collect enough training data!');
            return;
        }

        const confirmTrain = confirm(`Train ML models on ${stats.completedSessions} games?\n\nThis will enable Imitation Learning (Level 9) and Diffusion Policy (Level 10).`);
        
        if (!confirmTrain) return;

        const trainingData = this.dataCollector.getTrainingData();
        
        document.getElementById('trainingStatus').textContent = 'Training models...';
        document.getElementById('trainingStatus').style.display = 'block';

        // Small delay to let UI update
        await new Promise(resolve => setTimeout(resolve, 100));

        const results = await this.mlManager.trainModels(trainingData);

        if (results.imitationLearning) {
            LEVELS[8].unlocked = true; // Unlock level 9
            alert('✅ Imitation Learning model trained! Level 9 unlocked!');
        }

        if (results.diffusionPolicy) {
            LEVELS[9].unlocked = true; // Unlock level 10
            alert('✅ Diffusion Policy model trained! Level 10 unlocked!');
        }

        document.getElementById('trainingStatus').style.display = 'none';
        this.saveProgress();
        this.showLevelSelect();
    }

    showStatistics() {
        const stats = this.dataCollector.getStatistics();
        const message = `
📊 Gameplay Statistics

Total Games: ${stats.totalSessions}
Completed: ${stats.completedSessions}
Won: ${stats.wonSessions}
Win Rate: ${((stats.wonSessions / Math.max(stats.completedSessions, 1)) * 100).toFixed(1)}%

Average Duration: ${(stats.averageDuration / 1000).toFixed(1)}s
Average Efficiency: ${(stats.averageEfficiency * 100).toFixed(1)}%
Total Moves: ${stats.totalMoves}

Levels Completed: ${this.levelsCompleted.size}/${LEVELS.length}
        `;
        
        alert(message);
    }

    showLevelSelect() {
        document.getElementById('levelSelect').classList.remove('hidden');
        document.getElementById('gameOver').classList.add('hidden');
        
        const levelGrid = document.getElementById('levelGrid');
        levelGrid.innerHTML = '';

        LEVELS.forEach(level => {
            const levelCard = document.createElement('div');
            levelCard.className = `level-card ${level.unlocked ? '' : 'locked'}`;
            levelCard.style.borderColor = level.color;
            
            if (this.levelsCompleted.has(level.id)) {
                levelCard.classList.add('completed');
            }

            levelCard.innerHTML = `
                <div class="level-number">Level ${level.id}</div>
                <div class="level-name">${level.name}</div>
                <div class="level-desc">${level.description}</div>
                ${this.levelsCompleted.has(level.id) ? '<div class="level-star">⭐</div>' : ''}
                ${!level.unlocked ? '<div class="level-lock">🔒</div>' : ''}
            `;

            if (level.unlocked) {
                levelCard.addEventListener('click', () => this.startLevel(level.id));
            }

            levelGrid.appendChild(levelCard);
        });
    }

    saveProgress() {
        const progress = {
            levelsCompleted: Array.from(this.levelsCompleted),
            unlockedLevels: LEVELS.map((l, i) => ({ id: i + 1, unlocked: l.unlocked })),
            mlModels: this.mlManager.saveModels()
        };

        localStorage.setItem('mario_maze_progress', JSON.stringify(progress));
    }

    loadProgress() {
        try {
            const data = localStorage.getItem('mario_maze_progress');
            if (data) {
                const progress = JSON.parse(data);
                this.levelsCompleted = new Set(progress.levelsCompleted || []);
                
                if (progress.unlockedLevels) {
                    progress.unlockedLevels.forEach(l => {
                        if (LEVELS[l.id - 1]) {
                            LEVELS[l.id - 1].unlocked = l.unlocked;
                        }
                    });
                }

                if (progress.mlModels) {
                    this.mlManager.loadModels(progress.mlModels);
                }
            }
        } catch (e) {
            console.error('Failed to load progress:', e);
        }
    }

    drawMaze() {
        for (let y = 0; y < MAZE_ROWS; y++) {
            for (let x = 0; x < MAZE_COLS; x++) {
                const px = x * CELL_SIZE;
                const py = y * CELL_SIZE;

                if (this.maze[y][x] === 1) {
                    ctx.fillStyle = COLORS.wall;
                    ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
                    ctx.strokeStyle = COLORS.black;
                    ctx.lineWidth = 1;
                    ctx.strokeRect(px, py, CELL_SIZE, CELL_SIZE);
                } else {
                    ctx.fillStyle = COLORS.path;
                    ctx.fillRect(px, py, CELL_SIZE, CELL_SIZE);
                    ctx.strokeStyle = COLORS.pathBorder;
                    ctx.lineWidth = 1;
                    ctx.strokeRect(px, py, CELL_SIZE, CELL_SIZE);
                }
            }
        }

        const goalX = this.goalX * CELL_SIZE;
        const goalY = this.goalY * CELL_SIZE;
        ctx.fillStyle = COLORS.goal;
        ctx.fillRect(goalX, goalY, CELL_SIZE, CELL_SIZE);
        ctx.strokeStyle = COLORS.black;
        ctx.lineWidth = 2;
        ctx.strokeRect(goalX, goalY, CELL_SIZE, CELL_SIZE);

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
        ctx.fillStyle = COLORS.background;
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

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
const game = new EnhancedGame();
