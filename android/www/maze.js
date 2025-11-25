// Maze generation and pathfinding algorithms

class MazeGenerator {
    constructor(cols, rows) {
        this.cols = cols;
        this.rows = rows;
        this.grid = [];
    }

    generate() {
        // Initialize grid with walls
        for (let y = 0; y < this.rows; y++) {
            this.grid[y] = [];
            for (let x = 0; x < this.cols; x++) {
                this.grid[y][x] = 1; // 1 = wall
            }
        }

        // Depth-first search maze generation
        const stack = [[0, 0]];
        const visited = new Set(['0,0']);
        this.grid[0][0] = 0; // 0 = path

        const directions = [
            [0, -1], // Up
            [1, 0],  // Right
            [0, 1],  // Down
            [-1, 0]  // Left
        ];

        while (stack.length > 0) {
            const [currentX, currentY] = stack[stack.length - 1];
            const neighbors = [];

            for (const [dx, dy] of directions) {
                const nx = currentX + dx * 2;
                const ny = currentY + dy * 2;
                const key = `${nx},${ny}`;

                if (nx >= 0 && nx < this.cols && ny >= 0 && ny < this.rows && !visited.has(key)) {
                    neighbors.push([nx, ny, dx, dy]);
                }
            }

            if (neighbors.length > 0) {
                const [nx, ny, dx, dy] = neighbors[Math.floor(Math.random() * neighbors.length)];
                
                // Carve path
                this.grid[currentY + dy][currentX + dx] = 0;
                this.grid[ny][nx] = 0;
                
                visited.add(`${nx},${ny}`);
                stack.push([nx, ny]);
            } else {
                stack.pop();
            }
        }

        // Ensure start and goal are clear
        this.grid[0][0] = 0;
        this.grid[this.rows - 1][this.cols - 1] = 0;

        return this.grid;
    }
}

class PathFinder {
    constructor(maze) {
        this.maze = maze;
    }

    // Manhattan distance heuristic
    heuristic(pos, goal) {
        return Math.abs(pos[0] - goal[0]) + Math.abs(pos[1] - goal[1]);
    }

    // A* pathfinding algorithm
    findPath(start, goal) {
        const openSet = [[0, start]];
        const cameFrom = new Map();
        const gScore = new Map();
        const fScore = new Map();
        
        const startKey = `${start[0]},${start[1]}`;
        const goalKey = `${goal[0]},${goal[1]}`;
        
        gScore.set(startKey, 0);
        fScore.set(startKey, this.heuristic(start, goal));

        while (openSet.length > 0) {
            // Get node with lowest f score
            openSet.sort((a, b) => a[0] - b[0]);
            const [, current] = openSet.shift();
            const currentKey = `${current[0]},${current[1]}`;

            if (currentKey === goalKey) {
                // Reconstruct path
                const path = [];
                let curr = currentKey;
                while (cameFrom.has(curr)) {
                    const [x, y] = curr.split(',').map(Number);
                    path.unshift([x, y]);
                    curr = cameFrom.get(curr);
                }
                return path;
            }

            // Check neighbors
            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            for (const [dx, dy] of directions) {
                const neighbor = [current[0] + dx, current[1] + dy];
                const neighborKey = `${neighbor[0]},${neighbor[1]}`;

                if (neighbor[0] >= 0 && neighbor[0] < this.maze[0].length &&
                    neighbor[1] >= 0 && neighbor[1] < this.maze.length &&
                    this.maze[neighbor[1]][neighbor[0]] === 0) {

                    const tentativeG = gScore.get(currentKey) + 1;

                    if (!gScore.has(neighborKey) || tentativeG < gScore.get(neighborKey)) {
                        cameFrom.set(neighborKey, currentKey);
                        gScore.set(neighborKey, tentativeG);
                        fScore.set(neighborKey, tentativeG + this.heuristic(neighbor, goal));
                        
                        // Add to open set if not already there
                        if (!openSet.some(([, pos]) => pos[0] === neighbor[0] && pos[1] === neighbor[1])) {
                            openSet.push([fScore.get(neighborKey), neighbor]);
                        }
                    }
                }
            }
        }

        return [];
    }
}
