# Mario Maze Race - ML Features Guide

## 🎓 Overview

This enhanced version features **10 progressive difficulty levels** with different AI algorithms, culminating in **machine learning models that learn from YOUR gameplay**!

---

## 🎮 Game Levels

### **Level 1: A* Pathfinding** ⭐
- **Algorithm**: A* (A-Star)
- **Difficulty**: Easy
- **Speed**: Slow (8 frames/move)
- **Description**: Uses optimal pathfinding with Manhattan distance heuristic
- **How it works**: Always finds the shortest path by evaluating distance + cost

### **Level 2: Dijkstra's Algorithm** 🔵
- **Algorithm**: Dijkstra's Shortest Path
- **Difficulty**: Easy-Medium
- **Speed**: Medium-Slow (7 frames/move)
- **Description**: Uniform cost search without heuristic
- **How it works**: Explores all paths uniformly until goal is found

### **Level 3: Breadth-First Search (BFS)** 🟢
- **Algorithm**: BFS
- **Difficulty**: Medium
- **Speed**: Medium (6 frames/move)
- **Description**: Level-by-level maze exploration
- **How it works**: Explores maze layer by layer, guarantees shortest path

### **Level 4: Depth-First Search (DFS)** 🔴
- **Algorithm**: DFS
- **Difficulty**: Medium
- **Speed**: Fast (5 frames/move)
- **Description**: Deep exploration first approach
- **How it works**: Goes as deep as possible before backtracking

### **Level 5: Wall-Following** 🟠
- **Algorithm**: Right-Hand Rule
- **Difficulty**: Medium-Hard
- **Speed**: Very Fast (4 frames/move)
- **Description**: Classic maze-solving technique
- **How it works**: Keeps right hand on wall and follows it

### **Level 6: Q-Learning (RL)** 🟣
- **Algorithm**: Reinforcement Learning - Q-Learning
- **Difficulty**: Hard
- **Speed**: Medium (6 frames/move)
- **Description**: Learns optimal policy through trial and error
- **How it works**: Builds Q-table and uses epsilon-greedy exploration

### **Level 7: Genetic Algorithm** 🔵
- **Algorithm**: Evolutionary Computation
- **Difficulty**: Hard
- **Speed**: Medium-Slow (7 frames/move)
- **Description**: Evolution-based path optimization
- **How it works**: Population of paths evolves through selection, crossover, mutation

### **Level 8: Neural Network** 💗
- **Algorithm**: Simplified Deep Q-Network (DQN)
- **Difficulty**: Very Hard
- **Speed**: Fast (5 frames/move)
- **Description**: Pattern recognition with neural network
- **How it works**: Weighted combination of multiple factors

### **Level 9: Imitation Learning** 🟣 🤖
- **Algorithm**: Behavioral Cloning from User Data
- **Difficulty**: EXTREME
- **Speed**: Fast (5 frames/move)
- **Description**: **Learns from YOUR gameplay!**
- **How it works**: Neural network trained on your moves
- **Requirements**: Complete 5+ games and train models

### **Level 10: Diffusion Policy** 💜 🤖
- **Algorithm**: Advanced Diffusion Model
- **Difficulty**: ULTIMATE
- **Speed**: Very Fast (4 frames/move)
- **Description**: **State-of-the-art ML model**
- **How it works**: Denoising diffusion process for action generation
- **Requirements**: Complete 5+ games and train models

---

## 🤖 Machine Learning Features

### **Data Collection System**

Every move you make is automatically recorded:

- **Player position** at each step
- **AI position** for context
- **Maze state** snapshot
- **Actions taken** (up, down, left, right)
- **Rewards** calculated based on performance
- **Game duration** and efficiency metrics

### **Training Data Format**

```javascript
{
  states: [     // Encoded game states (10 features)
    [0.05, 0.07, 0.15, 0.2, ...],
    ...
  ],
  actions: [    // Actions taken (0=up, 1=right, 2=down, 3=left)
    2, 1, 1, 2, ...
  ],
  rewards: [    // Reward for each action
    -0.1, 1.0, -0.5, 100, ...
  ]
}
```

### **State Encoding (10 Features)**

1. **Player X** (normalized 0-1)
2. **Player Y** (normalized 0-1)
3. **AI X** (normalized 0-1)
4. **AI Y** (normalized 0-1)
5. **Distance to goal** (normalized)
6. **AI distance to goal** (normalized)
7. **Walls around player** (0-1)
8. **Walls around AI** (0-1)
9. **Time elapsed** (normalized)
10. **Random noise** (regularization)

---

## 🎓 Imitation Learning Model

### **Architecture**

```
Input (10 features)
    ↓
Hidden Layer 1 (32 neurons, ReLU)
    ↓
Hidden Layer 2 (32 neurons, ReLU)
    ↓
Output Layer (4 actions, Softmax)
```

### **Training Process**

1. Collects your gameplay data
2. Trains for 50 epochs
3. Uses supervised learning (behavioral cloning)
4. Minimizes cross-entropy loss
5. Learns to mimic your decisions

### **How to Train**

1. Play at least 5 complete games
2. Click "🤖 Train ML Models" button
3. Wait for training to complete (~5-10 seconds)
4. Level 9 unlocks automatically!

---

## 🌊 Diffusion Policy Model

### **Architecture**

```
Input (State + Noisy Action + Timestep)
    ↓
Denoising Network (3 layers)
    ↓
Noise Prediction
    ↓
Iterative Refinement (10 steps)
    ↓
Clean Action Output
```

### **How Diffusion Works**

1. **Forward Process**: Add noise to expert actions
2. **Training**: Learn to predict and remove noise
3. **Sampling**: Start from random noise
4. **Denoising**: Iteratively refine to clean action
5. **Output**: High-quality action prediction

### **Advantages**

- More robust than standard behavioral cloning
- Better generalization to new situations
- Handles multimodal action distributions
- State-of-the-art performance

---

## 📊 Statistics & Analytics

### **Tracked Metrics**

- **Total Sessions**: Number of games played
- **Completed Games**: Games finished (win or lose)
- **Won Games**: Games where you beat the AI
- **Win Rate**: Percentage of victories
- **Average Duration**: Time per game
- **Average Efficiency**: Optimal moves / actual moves
- **Total Moves**: All moves across all games

### **Viewing Statistics**

Click "📊 View Statistics" to see detailed analytics.

---

## 💾 Data Storage

All data is stored in browser's LocalStorage:

- **Gameplay sessions**: Last 100 games
- **ML model weights**: Trained neural networks
- **Progress data**: Unlocked levels, completed challenges
- **Training data**: Encoded states, actions, rewards

### **Data Export/Import**

```javascript
// Export data
const data = dataCollector.exportData();
// Returns JSON string

// Import data
dataCollector.importData(jsonString);
```

---

## 🎯 Reward System

### **Reward Calculation**

```python
base_reward = -0.1                    # Small penalty per move
progress_reward = +1.0                # Getting closer to goal
backtrack_penalty = -0.5              # Moving away from goal
win_reward = +100                     # Reaching the goal
```

### **Efficiency Score**

```
efficiency = optimal_path_length / actual_moves
```

A higher efficiency means you took a more direct route!

---

## 🔓 Level Unlocking System

### **Progression Rules**

1. **Level 1**: Always unlocked
2. **Levels 2-8**: Unlock by completing previous level
3. **Level 9**: Requires training ML models (5+ games)
4. **Level 10**: Requires training ML models (5+ games)

### **Completed Levels**

Completed levels show a ⭐ star badge and golden background.

---

## 🧠 Neural Network Details

### **Imitation Learning NN**

```
Parameters:
- Input neurons: 10
- Hidden layer 1: 32 neurons
- Hidden layer 2: 32 neurons
- Output neurons: 4
- Activation: ReLU (hidden), Softmax (output)
- Loss: Cross-Entropy
- Optimizer: SGD
- Learning rate: 0.01
- Epochs: 50
```

### **Diffusion Policy Network**

```
Parameters:
- Input neurons: 15 (state + action + timestep)
- Hidden layer 1: 32 neurons (tanh)
- Hidden layer 2: 32 neurons (tanh)
- Output neurons: 4
- Diffusion steps: 10
- Noise schedule: Linear (0.0001 to 0.02)
- Loss: MSE
- Learning rate: 0.001
- Epochs: 30
```

---

## 🚀 Advanced Usage

### **Custom Training**

```javascript
// Access the game instance
const game = window.game;

// Get training data
const trainingData = game.dataCollector.getTrainingData();

// Train models manually
await game.mlManager.trainModels(trainingData);

// Save trained models
const modelData = game.mlManager.saveModels();
localStorage.setItem('my_models', modelData);
```

### **Model Inspection**

```javascript
// Check if models are trained
game.mlManager.isModelTrained('imitation');  // true/false
game.mlManager.isModelTrained('diffusion');  // true/false

// Get prediction for current state
const state = game.dataCollector.encodeState(currentGameState);
const action = game.mlManager.predictAction(state, 'imitation');
// Returns: 0=up, 1=right, 2=down, 3=left
```

---

## 📈 Performance Tips

### **To Improve Win Rate**

1. Plan your route before moving
2. Take the shortest path possible
3. Don't backtrack unnecessarily
4. Learn from AI strategies
5. Practice on easier levels first

### **To Improve Training Data**

1. Play consistently (similar strategies)
2. Complete more games (quantity)
3. Win more often (quality)
4. Try different approaches
5. Avoid random movements

---

## 🔬 Research Applications

This game demonstrates:

- **Pathfinding algorithms** (A*, Dijkstra, BFS, DFS)
- **Heuristic search** methods
- **Reinforcement learning** (Q-Learning)
- **Evolutionary algorithms** (Genetic Algorithm)
- **Supervised learning** (Imitation Learning)
- **Generative models** (Diffusion Policy)
- **Behavioral cloning** techniques
- **Real-time ML inference** in browser

---

## 📚 Further Reading

### **Algorithms**

- **A***: Hart, P. E., Nilsson, N. J., & Raphael, B. (1968)
- **Q-Learning**: Watkins, C. J., & Dayan, P. (1992)
- **Genetic Algorithms**: Holland, J. H. (1992)
- **Diffusion Models**: Ho, J., et al. (2020)

### **Imitation Learning**

- **Behavioral Cloning**: Pomerleau, D. A. (1988)
- **DAgger**: Ross, S., Gordon, G., & Bagnell, D. (2011)

### **Diffusion Policies**

- **Diffusion Policy**: Chi, C., et al. (2023)
- **DDPM**: Ho, J., Jain, A., & Abbeel, P. (2020)

---

## 🎮 Quick Start

1. **Play Level 1-8**: Learn different AI algorithms
2. **Complete 5+ games**: Collect training data
3. **Train ML models**: Click the training button
4. **Challenge Level 9-10**: Beat your own trained AI!
5. **View stats**: Track your improvement

---

## 🏆 Achievement Goals

- ✅ Complete all 10 levels
- ✅ Train both ML models
- ✅ Achieve 70%+ win rate
- ✅ Average efficiency > 80%
- ✅ Beat diffusion policy AI

---

**The AI learns from YOU. Can you beat your own strategy?** 🤖🎮
