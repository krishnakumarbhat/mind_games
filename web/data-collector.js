// User Gameplay Data Collection and Storage

class GameplayDataCollector {
    constructor() {
        this.sessions = [];
        this.currentSession = null;
        this.storageKey = 'mario_maze_gameplay_data';
        this.loadFromStorage();
    }

    startSession(level, mazeData) {
        this.currentSession = {
            id: Date.now(),
            level: level,
            maze: mazeData,
            startTime: Date.now(),
            moves: [],
            states: [],
            actions: [],
            rewards: [],
            completed: false,
            won: false,
            duration: 0
        };
    }

    recordMove(fromPos, toPos, action) {
        if (!this.currentSession) return;

        const move = {
            timestamp: Date.now() - this.currentSession.startTime,
            from: [...fromPos],
            to: [...toPos],
            action: action, // 'up', 'down', 'left', 'right'
            distanceToGoal: this.calculateDistance(toPos, this.currentSession.goalPos || [19, 14])
        };

        this.currentSession.moves.push(move);
    }

    recordState(playerPos, aiPos, mazeState) {
        if (!this.currentSession) return;

        const state = {
            timestamp: Date.now() - this.currentSession.startTime,
            playerPos: [...playerPos],
            aiPos: [...aiPos],
            mazeSnapshot: JSON.parse(JSON.stringify(mazeState))
        };

        this.currentSession.states.push(state);
    }

    recordAction(action, reward) {
        if (!this.currentSession) return;

        this.currentSession.actions.push(action);
        this.currentSession.rewards.push(reward);
    }

    endSession(won, finalPos) {
        if (!this.currentSession) return;

        this.currentSession.completed = true;
        this.currentSession.won = won;
        this.currentSession.duration = Date.now() - this.currentSession.startTime;
        this.currentSession.finalPos = finalPos;
        this.currentSession.efficiency = this.calculateEfficiency();

        this.sessions.push(this.currentSession);
        this.saveToStorage();

        const sessionData = this.currentSession;
        this.currentSession = null;
        
        return sessionData;
    }

    calculateDistance(pos1, pos2) {
        return Math.abs(pos1[0] - pos2[0]) + Math.abs(pos1[1] - pos2[1]);
    }

    calculateEfficiency() {
        if (!this.currentSession || this.currentSession.moves.length === 0) return 0;

        const optimalMoves = this.currentSession.moves[0].distanceToGoal;
        const actualMoves = this.currentSession.moves.length;
        
        return optimalMoves / actualMoves;
    }

    getTrainingData() {
        // Convert sessions to training format for ML models
        const trainingData = {
            states: [],
            actions: [],
            rewards: [],
            nextStates: []
        };

        for (const session of this.sessions) {
            if (!session.completed) continue;

            for (let i = 0; i < session.moves.length - 1; i++) {
                const state = this.encodeState(session.states[i]);
                const action = this.encodeAction(session.moves[i].action);
                const reward = this.calculateReward(session.moves[i], session.won);
                const nextState = this.encodeState(session.states[i + 1]);

                trainingData.states.push(state);
                trainingData.actions.push(action);
                trainingData.rewards.push(reward);
                trainingData.nextStates.push(nextState);
            }
        }

        return trainingData;
    }

    encodeState(state) {
        if (!state) return new Array(10).fill(0);

        // Encode state as feature vector
        return [
            state.playerPos[0] / 20,
            state.playerPos[1] / 15,
            state.aiPos[0] / 20,
            state.aiPos[1] / 15,
            this.calculateDistance(state.playerPos, [19, 14]) / 35,
            this.calculateDistance(state.aiPos, [19, 14]) / 35,
            this.countSurroundingWalls(state.playerPos, state.mazeSnapshot) / 4,
            this.countSurroundingWalls(state.aiPos, state.mazeSnapshot) / 4,
            state.timestamp / 60000, // Normalize time
            Math.random() * 0.1 // Add small noise for regularization
        ];
    }

    encodeAction(action) {
        const actionMap = { 'up': 0, 'right': 1, 'down': 2, 'left': 3 };
        return actionMap[action] || 0;
    }

    calculateReward(move, won) {
        let reward = -0.1; // Small penalty for each move

        // Reward for getting closer to goal
        if (move.from && move.to) {
            const prevDist = this.calculateDistance(move.from, [19, 14]);
            const newDist = move.distanceToGoal;
            
            if (newDist < prevDist) {
                reward += 1; // Reward for progress
            } else if (newDist > prevDist) {
                reward -= 0.5; // Penalty for moving away
            }
        }

        // Big reward for winning
        if (won && move === this.currentSession?.moves[this.currentSession.moves.length - 1]) {
            reward += 100;
        }

        return reward;
    }

    countSurroundingWalls(pos, maze) {
        if (!maze) return 0;
        
        const directions = [[0, -1], [1, 0], [0, 1], [-1, 0]];
        let count = 0;

        for (const [dx, dy] of directions) {
            const nx = pos[0] + dx;
            const ny = pos[1] + dy;
            
            if (nx < 0 || nx >= 20 || ny < 0 || ny >= 15 || maze[ny][nx] === 1) {
                count++;
            }
        }

        return count;
    }

    getStatistics() {
        return {
            totalSessions: this.sessions.length,
            completedSessions: this.sessions.filter(s => s.completed).length,
            wonSessions: this.sessions.filter(s => s.won).length,
            averageDuration: this.sessions.reduce((sum, s) => sum + (s.duration || 0), 0) / Math.max(this.sessions.length, 1),
            averageEfficiency: this.sessions.reduce((sum, s) => sum + (s.efficiency || 0), 0) / Math.max(this.sessions.length, 1),
            totalMoves: this.sessions.reduce((sum, s) => sum + s.moves.length, 0)
        };
    }

    saveToStorage() {
        try {
            // Keep only last 100 sessions to prevent storage overflow
            const sessionsToSave = this.sessions.slice(-100);
            localStorage.setItem(this.storageKey, JSON.stringify(sessionsToSave));
        } catch (e) {
            console.warn('Failed to save gameplay data:', e);
        }
    }

    loadFromStorage() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (data) {
                this.sessions = JSON.parse(data);
            }
        } catch (e) {
            console.warn('Failed to load gameplay data:', e);
            this.sessions = [];
        }
    }

    clearData() {
        this.sessions = [];
        this.currentSession = null;
        localStorage.removeItem(this.storageKey);
    }

    exportData() {
        return JSON.stringify({
            sessions: this.sessions,
            statistics: this.getStatistics(),
            exportDate: new Date().toISOString()
        }, null, 2);
    }

    importData(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            if (data.sessions) {
                this.sessions = data.sessions;
                this.saveToStorage();
                return true;
            }
        } catch (e) {
            console.error('Failed to import data:', e);
        }
        return false;
    }
}
