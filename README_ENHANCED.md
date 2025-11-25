# 🍄 Mario Maze Race - ML Enhanced Edition

## 🎮 What's New?

This enhanced version transforms the simple maze game into a **comprehensive AI and Machine Learning educational platform** with:

- **10 Progressive Difficulty Levels** with different AI algorithms
- **Automatic Gameplay Data Collection** 
- **Imitation Learning** that learns from YOUR playstyle
- **Diffusion Policy** - State-of-the-art generative AI model
- **Level Progression System** with unlockables
- **Detailed Statistics** and performance tracking
- **Beautiful Modern UI** with animations

---

## 🚀 Quick Start - Enhanced Version

### **Web Version** (Recommended for ML Features)

```bash
cd web
python -m http.server 8001
```

Then open `http://localhost:8001/index-enhanced.html`

**Note**: Use `index-enhanced.html` for the ML version!

---

## 🎯 Game Levels Overview

| Level | AI Algorithm | Difficulty | Speed | Unlocking |
|-------|-------------|------------|-------|-----------|
| 1 | A* Pathfinding | ⭐ Easy | Slow | Unlocked |
| 2 | Dijkstra | ⭐⭐ Easy-Med | Med-Slow | Beat Level 1 |
| 3 | BFS | ⭐⭐ Medium | Medium | Beat Level 2 |
| 4 | DFS | ⭐⭐⭐ Medium | Fast | Beat Level 3 |
| 5 | Wall-Following | ⭐⭐⭐ Med-Hard | V.Fast | Beat Level 4 |
| 6 | Q-Learning (RL) | ⭐⭐⭐⭐ Hard | Medium | Beat Level 5 |
| 7 | Genetic Algorithm | ⭐⭐⭐⭐ Hard | Med-Slow | Beat Level 6 |
| 8 | Neural Network | ⭐⭐⭐⭐⭐ V.Hard | Fast | Beat Level 7 |
| 9 | **Imitation Learning** | 🤖 EXTREME | Fast | Train ML Models |
| 10 | **Diffusion Policy** | 🤖 ULTIMATE | V.Fast | Train ML Models |

---

## 🤖 Machine Learning Features

### **1. Automatic Data Collection**

Every move you make is recorded:
- Player and AI positions
- Maze state
- Actions taken
- Rewards calculated
- Performance metrics

### **2. Imitation Learning Model**

- **Type**: Behavioral Cloning Neural Network
- **Architecture**: 10 input → 32 → 32 → 4 output
- **Training**: 50 epochs on your gameplay
- **Purpose**: Learns to mimic your decision-making

### **3. Diffusion Policy Model**

- **Type**: Denoising Diffusion Probabilistic Model
- **Architecture**: 15 input → 32 → 32 → 4 output
- **Training**: 30 epochs with diffusion process
- **Purpose**: State-of-the-art action generation

### **4. How to Train Models**

1. **Play 5+ games** to collect training data
2. Click **"🤖 Train ML Models"** button
3. Wait ~10 seconds for training
4. **Levels 9 & 10 unlock** automatically!
5. Challenge the AI that learned from YOU!

---

## 📊 Statistics & Progress Tracking

Track your improvement with:
- **Total Games Played**
- **Win Rate**
- **Average Efficiency** (optimal moves / actual moves)
- **Average Duration**
- **Levels Completed**
- **Training Data Collected**

Access via **"📊 View Statistics"** button.

---

## 🎓 Educational Value

### **Computer Science Concepts**

1. **Graph Algorithms**
   - A* Pathfinding
   - Dijkstra's Algorithm
   - Breadth-First Search
   - Depth-First Search

2. **Heuristic Search**
   - Manhattan distance heuristic
   - Admissible heuristics
   - Optimal vs. complete algorithms

3. **Reinforcement Learning**
   - Q-Learning
   - Temporal Difference Learning
   - Exploration vs. Exploitation

4. **Evolutionary Computation**
   - Genetic Algorithms
   - Selection, Crossover, Mutation
   - Fitness functions

5. **Machine Learning**
   - Neural Networks
   - Supervised Learning
   - Behavioral Cloning
   - Generative Models

6. **Advanced ML**
   - Imitation Learning
   - Diffusion Models
   - Policy Learning
   - Real-time Inference

---

## 📁 Enhanced File Structure

```
web/
├── index-enhanced.html         # Enhanced ML version entry point
├── styles-enhanced.css         # Enhanced UI styles
├── maze.js                     # Maze generation (unchanged)
├── ai-algorithms.js            # NEW: 8 AI algorithms
├── data-collector.js           # NEW: Gameplay data collection
├── ml-models.js                # NEW: ML training & inference
├── game-enhanced.js            # NEW: Multi-level game logic
└── README.md
```

---

## 🔬 Technical Implementation

### **State Encoding (10 Features)**

```javascript
[
  playerX / 20,              // Normalized player X
  playerY / 15,              // Normalized player Y  
  aiX / 20,                  // Normalized AI X
  aiY / 15,                  // Normalized AI Y
  playerDistToGoal / 35,     // Normalized distance
  aiDistToGoal / 35,         // Normalized AI distance
  surroundingWalls / 4,      // Wall density around player
  aiSurroundingWalls / 4,    // Wall density around AI
  timeElapsed / 60000,       // Normalized time
  randomNoise * 0.1          // Regularization
]
```

### **Action Encoding**

```javascript
0 = UP
1 = RIGHT
2 = DOWN
3 = LEFT
```

### **Reward Structure**

```javascript
-0.1   // Base penalty per move
+1.0   // Reward for getting closer to goal
-0.5   // Penalty for moving away from goal
+100   // Big reward for reaching goal
```

---

## 🎮 Gameplay Tips

### **For Beginners**

1. Start with Level 1 (A*) - it's optimal but slow
2. Learn the maze patterns
3. Plan your route before moving
4. Don't rush - think strategically

### **For Advanced Players**

1. Study each AI algorithm's behavior
2. Complete all 8 classic levels
3. Play 10+ games for better training data
4. Train ML models with diverse gameplay
5. Challenge yourself against your own AI!

### **For ML Training**

1. **Consistent Strategy**: Play with similar patterns
2. **Quality over Quantity**: Win more games
3. **Diverse Scenarios**: Try different mazes
4. **Complete Games**: Finish games (even if you lose)
5. **5+ Games Minimum**: More data = better models

---

## 💾 Data Persistence

All data is saved in **browser LocalStorage**:

- Gameplay history (last 100 sessions)
- Trained ML model weights
- Level progress & unlocks
- Statistics & achievements

**Note**: Clearing browser data will reset progress!

---

## 🌐 Browser Compatibility

### **Minimum Requirements**

- Modern browser with ES6 support
- LocalStorage enabled
- Canvas API support

### **Tested Browsers**

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ Opera 76+

---

## 📈 Performance

### **Training Performance**

- **Imitation Learning**: ~5-10 seconds
- **Diffusion Policy**: ~8-15 seconds
- **Inference**: Real-time (<16ms per action)

### **Memory Usage**

- Base game: ~10 MB
- With 100 sessions: ~15 MB
- Trained models: ~2 MB

---

## 🔧 Customization

### **Adjust AI Difficulty**

Edit `LEVELS` array in `game-enhanced.js`:

```javascript
{ 
  id: 1, 
  name: 'A* Pathfinding', 
  algorithm: 'aStar', 
  speed: 8,  // Increase = slower AI
  color: COLORS.luigi 
}
```

### **Change Training Parameters**

In `ml-models.js`:

```javascript
// Imitation Learning
train(trainingData, epochs = 50)  // Increase epochs

// Diffusion Policy
this.diffusionSteps = 10;  // Increase steps
```

---

## 🐛 Troubleshooting

### **"Not enough training data"**

- Play at least 5 complete games
- Make sure games are completed (reach goal or AI wins)

### **"ML models not working"**

- Check browser console for errors
- Ensure LocalStorage is enabled
- Try clearing browser cache
- Retrain models

### **"Levels not unlocking"**

- Complete previous levels first
- For Level 9-10: Train ML models
- Check localStorage for save data

### **"Game running slow"**

- Close other browser tabs
- Refresh the page
- Check browser's performance settings

---

## 📚 Learning Resources

### **Algorithms**

- [A* Pathfinding Tutorial](https://www.redblobgames.com/pathfinding/a-star/)
- [Reinforcement Learning Introduction](https://spinningup.openai.com/)
- [Genetic Algorithms Explained](https://towardsdatascience.com/genetic-algorithms)

### **Machine Learning**

- [Imitation Learning Survey](https://arxiv.org/abs/1811.06711)
- [Diffusion Models](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
- [Behavioral Cloning](https://www.cs.cmu.edu/~tom/10701_sp11/slides/BC.pdf)

---

## 🏆 Achievements

Can you complete all of these?

- ✅ **Beginner**: Complete Level 1
- ✅ **Apprentice**: Complete Levels 1-4
- ✅ **Expert**: Complete Levels 1-8
- ✅ **Data Scientist**: Collect 50+ game sessions
- ✅ **ML Master**: Train both ML models
- ✅ **Perfectionist**: Achieve 90%+ efficiency
- ✅ **Unbeatable**: Win against Diffusion Policy AI
- ✅ **Completionist**: 100% all levels

---

## 🎓 For Educators

This game is perfect for teaching:

- **Intro to CS**: Basic algorithms (BFS, DFS)
- **AI Course**: Search algorithms, heuristics
- **ML Course**: Neural networks, behavioral cloning
- **Advanced ML**: Diffusion models, policy learning
- **Game Dev**: Browser-based game development
- **Web Dev**: Modern JavaScript, HTML5 Canvas

**Free for educational use!**

---

## 🤝 Contributing

Want to add more features?

1. Fork the repository
2. Add new AI algorithms
3. Improve ML models
4. Create better visualizations
5. Optimize performance
6. Submit pull request

---

## 📄 License

MIT License - Free to use, modify, and distribute

---

## 🎉 Credits

**Original Game**: Mario Maze Race
**Enhanced ML Version**: Created with educational purpose
**Algorithms**: Classic CS and modern ML techniques
**Inspiration**: Super Mario Bros (Nintendo)

---

## 📞 Support

Having issues?

1. Check ML_FEATURES_GUIDE.md
2. Read troubleshooting section
3. Check browser console
4. Verify all files are loaded

---

## 🔮 Future Enhancements

Potential additions:

- [ ] More AI algorithms (Monte Carlo Tree Search)
- [ ] Multi-player mode
- [ ] Online leaderboards
- [ ] Model comparison tool
- [ ] Advanced visualizations (heatmaps)
- [ ] Export trained models
- [ ] Mobile app version with ML
- [ ] Tournament mode
- [ ] Custom maze editor

---

## 🎮 Start Playing!

```bash
cd web
python -m http.server 8001
# Open http://localhost:8001/index-enhanced.html
```

**Beat 8 AI algorithms, then train your own!** 🤖🎯

---

**The ultimate challenge: Can you beat an AI that learned from YOU?** 🏆
