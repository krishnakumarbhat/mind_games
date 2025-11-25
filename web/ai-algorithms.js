// Advanced AI Algorithms for Multi-Level Maze Game

class AIAlgorithms {
    constructor(maze) {
        this.maze = maze;
        this.rows = maze.length;
        this.cols = maze[0].length;
    }

    // Level 1: A* Algorithm (Optimal Pathfinding)
    aStar(start, goal) {
        const openSet = [[0, start]];
        const cameFrom = new Map();
        const gScore = new Map();
        const fScore = new Map();
        
        const startKey = `${start[0]},${start[1]}`;
        const goalKey = `${goal[0]},${goal[1]}`;
        
        gScore.set(startKey, 0);
        fScore.set(startKey, this.heuristic(start, goal));

        while (openSet.length > 0) {
            openSet.sort((a, b) => a[0] - b[0]);
            const [, current] = openSet.shift();
            const currentKey = `${current[0]},${current[1]}`;

            if (currentKey === goalKey) {
                return this.reconstructPath(cameFrom, currentKey);
            }

            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            for (const [dx, dy] of directions) {
                const neighbor = [current[0] + dx, current[1] + dy];
                const neighborKey = `${neighbor[0]},${neighbor[1]}`;

                if (this.isValidCell(neighbor)) {
                    const tentativeG = gScore.get(currentKey) + 1;

                    if (!gScore.has(neighborKey) || tentativeG < gScore.get(neighborKey)) {
                        cameFrom.set(neighborKey, currentKey);
                        gScore.set(neighborKey, tentativeG);
                        fScore.set(neighborKey, tentativeG + this.heuristic(neighbor, goal));
                        
                        if (!openSet.some(([, pos]) => pos[0] === neighbor[0] && pos[1] === neighbor[1])) {
                            openSet.push([fScore.get(neighborKey), neighbor]);
                        }
                    }
                }
            }
        }
        return [];
    }

    // Level 2: Dijkstra's Algorithm (Uniform Cost Search)
    dijkstra(start, goal) {
        const distances = new Map();
        const cameFrom = new Map();
        const unvisited = [];
        
        const startKey = `${start[0]},${start[1]}`;
        const goalKey = `${goal[0]},${goal[1]}`;
        
        distances.set(startKey, 0);
        unvisited.push([0, start]);

        while (unvisited.length > 0) {
            unvisited.sort((a, b) => a[0] - b[0]);
            const [currentDist, current] = unvisited.shift();
            const currentKey = `${current[0]},${current[1]}`;

            if (currentKey === goalKey) {
                return this.reconstructPath(cameFrom, currentKey);
            }

            if (currentDist > (distances.get(currentKey) || Infinity)) {
                continue;
            }

            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            for (const [dx, dy] of directions) {
                const neighbor = [current[0] + dx, current[1] + dy];
                const neighborKey = `${neighbor[0]},${neighbor[1]}`;

                if (this.isValidCell(neighbor)) {
                    const newDist = currentDist + 1;
                    
                    if (newDist < (distances.get(neighborKey) || Infinity)) {
                        distances.set(neighborKey, newDist);
                        cameFrom.set(neighborKey, currentKey);
                        unvisited.push([newDist, neighbor]);
                    }
                }
            }
        }
        return [];
    }

    // Level 3: Breadth-First Search (BFS)
    bfs(start, goal) {
        const queue = [[start]];
        const visited = new Set([`${start[0]},${start[1]}`]);
        const goalKey = `${goal[0]},${goal[1]}`;

        while (queue.length > 0) {
            const path = queue.shift();
            const current = path[path.length - 1];
            const currentKey = `${current[0]},${current[1]}`;

            if (currentKey === goalKey) {
                return path.slice(1); // Remove start position
            }

            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            for (const [dx, dy] of directions) {
                const neighbor = [current[0] + dx, current[1] + dy];
                const neighborKey = `${neighbor[0]},${neighbor[1]}`;

                if (this.isValidCell(neighbor) && !visited.has(neighborKey)) {
                    visited.add(neighborKey);
                    queue.push([...path, neighbor]);
                }
            }
        }
        return [];
    }

    // Level 4: Depth-First Search (DFS)
    dfs(start, goal) {
        const stack = [[start]];
        const visited = new Set();
        const goalKey = `${goal[0]},${goal[1]}`;

        while (stack.length > 0) {
            const path = stack.pop();
            const current = path[path.length - 1];
            const currentKey = `${current[0]},${current[1]}`;

            if (visited.has(currentKey)) continue;
            visited.add(currentKey);

            if (currentKey === goalKey) {
                return path.slice(1);
            }

            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            for (const [dx, dy] of directions) {
                const neighbor = [current[0] + dx, current[1] + dy];
                const neighborKey = `${neighbor[0]},${neighbor[1]}`;

                if (this.isValidCell(neighbor) && !visited.has(neighborKey)) {
                    stack.push([...path, neighbor]);
                }
            }
        }
        return [];
    }

    // Level 5: Wall-Following Algorithm (Right-Hand Rule)
    wallFollowing(start, goal) {
        const path = [start];
        let current = [...start];
        let direction = 0; // 0=North, 1=East, 2=South, 3=West
        const visited = new Set([`${start[0]},${start[1]}`]);
        const goalKey = `${goal[0]},${goal[1]}`;
        const maxSteps = this.rows * this.cols * 4; // Prevent infinite loops
        let steps = 0;

        const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];

        while (steps < maxSteps) {
            const currentKey = `${current[0]},${current[1]}`;
            
            if (currentKey === goalKey) {
                return path.slice(1);
            }

            // Try to turn right first
            const rightDir = (direction + 1) % 4;
            const [rdx, rdy] = directions[rightDir];
            const rightCell = [current[0] + rdx, current[1] + rdy];

            if (this.isValidCell(rightCell)) {
                // Turn right and move
                direction = rightDir;
                current = rightCell;
            } else {
                // Try forward
                const [fdx, fdy] = directions[direction];
                const forwardCell = [current[0] + fdx, current[1] + fdy];

                if (this.isValidCell(forwardCell)) {
                    current = forwardCell;
                } else {
                    // Turn left
                    direction = (direction + 3) % 4;
                    continue;
                }
            }

            const nextKey = `${current[0]},${current[1]}`;
            if (!visited.has(nextKey)) {
                visited.add(nextKey);
                path.push([...current]);
            }
            steps++;
        }

        // If wall-following doesn't reach goal, fall back to A*
        return this.aStar(start, goal);
    }

    // Level 6: Reinforcement Learning (Q-Learning Simulation)
    reinforcementLearning(start, goal) {
        // Simulated Q-learning with pre-trained Q-table
        // In real implementation, this would be trained over many episodes
        const qTable = new Map();
        const alpha = 0.1; // Learning rate
        const gamma = 0.9; // Discount factor
        const episodes = 50; // Quick training

        // Initialize Q-values
        for (let y = 0; y < this.rows; y++) {
            for (let x = 0; x < this.cols; x++) {
                if (this.maze[y][x] === 0) {
                    const key = `${x},${y}`;
                    qTable.set(key, [0, 0, 0, 0]); // Up, Right, Down, Left
                }
            }
        }

        // Quick training phase
        for (let episode = 0; episode < episodes; episode++) {
            let current = [...start];
            const visited = new Set();
            const maxSteps = 100;

            for (let step = 0; step < maxSteps; step++) {
                const currentKey = `${current[0]},${current[1]}`;
                if (currentKey === `${goal[0]},${goal[1]}`) break;

                const qValues = qTable.get(currentKey) || [0, 0, 0, 0];
                const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
                
                // Epsilon-greedy action selection
                const epsilon = 0.1;
                let action;
                if (Math.random() < epsilon) {
                    action = Math.floor(Math.random() * 4);
                } else {
                    action = qValues.indexOf(Math.max(...qValues));
                }

                const [dx, dy] = directions[action];
                const next = [current[0] + dx, current[1] + dy];
                const nextKey = `${next[0]},${next[1]}`;

                if (this.isValidCell(next)) {
                    const reward = nextKey === `${goal[0]},${goal[1]}` ? 100 : -1;
                    const nextQValues = qTable.get(nextKey) || [0, 0, 0, 0];
                    const maxNextQ = Math.max(...nextQValues);
                    
                    qValues[action] = qValues[action] + alpha * (reward + gamma * maxNextQ - qValues[action]);
                    qTable.set(currentKey, qValues);
                    
                    current = next;
                } else {
                    qValues[action] -= 10; // Penalty for hitting wall
                    qTable.set(currentKey, qValues);
                }
            }
        }

        // Use trained Q-table to find path
        const path = [];
        let current = [...start];
        const visited = new Set();
        const maxSteps = this.rows * this.cols;

        for (let step = 0; step < maxSteps; step++) {
            const currentKey = `${current[0]},${current[1]}`;
            
            if (currentKey === `${goal[0]},${goal[1]}`) {
                return path;
            }

            if (visited.has(currentKey)) break;
            visited.add(currentKey);

            const qValues = qTable.get(currentKey) || [0, 0, 0, 0];
            const action = qValues.indexOf(Math.max(...qValues));
            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            const [dx, dy] = directions[action];
            const next = [current[0] + dx, current[1] + dy];

            if (this.isValidCell(next)) {
                path.push(next);
                current = next;
            } else {
                break;
            }
        }

        // Fallback to A* if RL doesn't find complete path
        if (path.length === 0 || `${current[0]},${current[1]}` !== `${goal[0]},${goal[1]}`) {
            return this.aStar(start, goal);
        }

        return path;
    }

    // Level 7: Genetic Algorithm
    geneticAlgorithm(start, goal) {
        const populationSize = 20;
        const generations = 30;
        const mutationRate = 0.1;

        // Generate random path length estimate
        const maxPathLength = this.rows * this.cols;

        // Initialize population with random paths
        let population = this.initializePopulation(populationSize, start, goal, maxPathLength);

        for (let gen = 0; gen < generations; gen++) {
            // Evaluate fitness
            const fitness = population.map(path => this.evaluatePathFitness(path, goal));

            // Select parents
            const parents = this.selectParents(population, fitness);

            // Create new generation
            const newPopulation = [];
            while (newPopulation.length < populationSize) {
                const parent1 = parents[Math.floor(Math.random() * parents.length)];
                const parent2 = parents[Math.floor(Math.random() * parents.length)];
                
                let child = this.crossover(parent1, parent2);
                child = this.mutate(child, mutationRate, start, goal);
                
                newPopulation.push(child);
            }

            population = newPopulation;
        }

        // Return best path
        const fitness = population.map(path => this.evaluatePathFitness(path, goal));
        const bestIndex = fitness.indexOf(Math.max(...fitness));
        const bestPath = population[bestIndex];

        // Validate path, fallback to A* if invalid
        if (this.isValidPath(bestPath, start, goal)) {
            return bestPath.slice(1);
        }
        return this.aStar(start, goal);
    }

    // Level 8: Neural Network (Simplified DQN)
    neuralNetwork(start, goal) {
        // Simplified neural network using pattern recognition
        // In production, this would be a trained deep Q-network
        
        const features = this.extractFeatures(start, goal);
        const path = [];
        let current = [...start];
        const visited = new Set([`${start[0]},${start[1]}`]);
        const maxSteps = this.rows * this.cols;

        for (let step = 0; step < maxSteps; step++) {
            const currentKey = `${current[0]},${current[1]}`;
            
            if (currentKey === `${goal[0]},${goal[1]}`) {
                return path;
            }

            // Neural network decision (simplified)
            const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
            let bestAction = 0;
            let bestScore = -Infinity;

            for (let i = 0; i < 4; i++) {
                const [dx, dy] = directions[i];
                const next = [current[0] + dx, current[1] + dy];
                const nextKey = `${next[0]},${next[1]}`;

                if (this.isValidCell(next) && !visited.has(nextKey)) {
                    // Calculate score based on multiple factors
                    const distToGoal = this.heuristic(next, goal);
                    const wallCount = this.countSurroundingWalls(next);
                    const progressScore = this.heuristic(current, goal) - distToGoal;
                    
                    // Neural network-like weighted combination
                    const score = (progressScore * 10) - (distToGoal * 5) - (wallCount * 2) + (Math.random() * 0.5);
                    
                    if (score > bestScore) {
                        bestScore = score;
                        bestAction = i;
                    }
                }
            }

            const [dx, dy] = directions[bestAction];
            const next = [current[0] + dx, current[1] + dy];
            const nextKey = `${next[0]},${next[1]}`;

            if (this.isValidCell(next) && !visited.has(nextKey)) {
                visited.add(nextKey);
                path.push(next);
                current = next;
            } else {
                // Stuck, fallback to A*
                const remainingPath = this.aStar(current, goal);
                return [...path, ...remainingPath];
            }
        }

        return this.aStar(start, goal);
    }

    // Helper methods
    heuristic(pos, goal) {
        return Math.abs(pos[0] - goal[0]) + Math.abs(pos[1] - goal[1]);
    }

    isValidCell(pos) {
        return pos[0] >= 0 && pos[0] < this.cols &&
               pos[1] >= 0 && pos[1] < this.rows &&
               this.maze[pos[1]][pos[0]] === 0;
    }

    reconstructPath(cameFrom, currentKey) {
        const path = [];
        let curr = currentKey;
        while (cameFrom.has(curr)) {
            const [x, y] = curr.split(',').map(Number);
            path.unshift([x, y]);
            curr = cameFrom.get(curr);
        }
        return path;
    }

    countSurroundingWalls(pos) {
        const directions = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]];
        let count = 0;
        for (const [dx, dy] of directions) {
            const next = [pos[0] + dx, pos[1] + dy];
            if (next[0] < 0 || next[0] >= this.cols || next[1] < 0 || next[1] >= this.rows || 
                this.maze[next[1]][next[0]] === 1) {
                count++;
            }
        }
        return count;
    }

    extractFeatures(start, goal) {
        return {
            manhattanDist: this.heuristic(start, goal),
            euclideanDist: Math.sqrt(Math.pow(start[0] - goal[0], 2) + Math.pow(start[1] - goal[1], 2)),
            wallDensity: this.countSurroundingWalls(start) / 8
        };
    }

    // GA helper methods
    initializePopulation(size, start, goal, maxLength) {
        const population = [];
        for (let i = 0; i < size; i++) {
            const path = this.generateRandomPath(start, goal, maxLength);
            population.push(path);
        }
        return population;
    }

    generateRandomPath(start, goal, maxLength) {
        const path = [start];
        let current = [...start];
        const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
        
        for (let i = 0; i < maxLength && `${current[0]},${current[1]}` !== `${goal[0]},${goal[1]}`; i++) {
            const validMoves = directions
                .map(([dx, dy]) => [current[0] + dx, current[1] + dy])
                .filter(pos => this.isValidCell(pos));
            
            if (validMoves.length === 0) break;
            
            current = validMoves[Math.floor(Math.random() * validMoves.length)];
            path.push([...current]);
        }
        
        return path;
    }

    evaluatePathFitness(path, goal) {
        if (path.length === 0) return -1000;
        
        const lastPos = path[path.length - 1];
        const distToGoal = this.heuristic(lastPos, goal);
        const pathLength = path.length;
        
        // Fitness: closer to goal = better, shorter path = better
        return 1000 / (distToGoal + 1) - pathLength * 0.1;
    }

    selectParents(population, fitness) {
        const parents = [];
        const totalFitness = fitness.reduce((sum, f) => sum + Math.max(f, 0), 0);
        
        for (let i = 0; i < population.length / 2; i++) {
            let rand = Math.random() * totalFitness;
            let sum = 0;
            
            for (let j = 0; j < population.length; j++) {
                sum += Math.max(fitness[j], 0);
                if (sum >= rand) {
                    parents.push(population[j]);
                    break;
                }
            }
        }
        
        return parents;
    }

    crossover(parent1, parent2) {
        const cutPoint = Math.floor(Math.min(parent1.length, parent2.length) / 2);
        return [...parent1.slice(0, cutPoint), ...parent2.slice(cutPoint)];
    }

    mutate(path, rate, start, goal) {
        if (Math.random() > rate || path.length < 2) return path;
        
        const mutateIndex = Math.floor(Math.random() * path.length);
        const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
        const [dx, dy] = directions[Math.floor(Math.random() * 4)];
        
        const newPos = [path[mutateIndex][0] + dx, path[mutateIndex][1] + dy];
        if (this.isValidCell(newPos)) {
            path[mutateIndex] = newPos;
        }
        
        return path;
    }

    isValidPath(path, start, goal) {
        if (path.length === 0) return false;
        if (`${path[0][0]},${path[0][1]}` !== `${start[0]},${start[1]}`) return false;
        
        for (const pos of path) {
            if (!this.isValidCell(pos)) return false;
        }
        
        return true;
    }
}
