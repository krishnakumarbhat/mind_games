// Machine Learning Models: Imitation Learning and Diffusion Policy

class ImitationLearningModel {
    constructor() {
        this.model = null;
        this.trained = false;
        this.neurons = 32;
        this.learningRate = 0.01;
        
        // Simple neural network weights
        this.weights = {
            layer1: this.initializeWeights(10, this.neurons),
            layer2: this.initializeWeights(this.neurons, this.neurons),
            output: this.initializeWeights(this.neurons, 4) // 4 actions
        };
        
        this.biases = {
            layer1: new Array(this.neurons).fill(0),
            layer2: new Array(this.neurons).fill(0),
            output: new Array(4).fill(0)
        };
    }

    initializeWeights(inputSize, outputSize) {
        const weights = [];
        for (let i = 0; i < inputSize; i++) {
            weights[i] = [];
            for (let j = 0; j < outputSize; j++) {
                weights[i][j] = (Math.random() - 0.5) * 0.1;
            }
        }
        return weights;
    }

    train(trainingData, epochs = 50) {
        console.log(`Training Imitation Learning model on ${trainingData.states.length} samples...`);
        
        if (trainingData.states.length < 10) {
            console.warn('Not enough training data. Need at least 10 samples.');
            return false;
        }

        for (let epoch = 0; epoch < epochs; epoch++) {
            let totalLoss = 0;

            // Shuffle training data
            const indices = Array.from({length: trainingData.states.length}, (_, i) => i);
            this.shuffle(indices);

            for (const idx of indices) {
                const state = trainingData.states[idx];
                const targetAction = trainingData.actions[idx];
                
                // Forward pass
                const prediction = this.forward(state);
                
                // Calculate loss
                const loss = this.crossEntropyLoss(prediction, targetAction);
                totalLoss += loss;
                
                // Backward pass
                this.backward(state, prediction, targetAction);
            }

            if (epoch % 10 === 0) {
                console.log(`Epoch ${epoch}: Loss = ${(totalLoss / trainingData.states.length).toFixed(4)}`);
            }
        }

        this.trained = true;
        console.log('Imitation Learning model trained successfully!');
        return true;
    }

    forward(state) {
        // Layer 1
        let hidden1 = new Array(this.neurons).fill(0);
        for (let j = 0; j < this.neurons; j++) {
            let sum = this.biases.layer1[j];
            for (let i = 0; i < state.length; i++) {
                sum += state[i] * this.weights.layer1[i][j];
            }
            hidden1[j] = this.relu(sum);
        }

        // Layer 2
        let hidden2 = new Array(this.neurons).fill(0);
        for (let j = 0; j < this.neurons; j++) {
            let sum = this.biases.layer2[j];
            for (let i = 0; i < this.neurons; i++) {
                sum += hidden1[i] * this.weights.layer2[i][j];
            }
            hidden2[j] = this.relu(sum);
        }

        // Output layer
        let output = new Array(4).fill(0);
        for (let j = 0; j < 4; j++) {
            let sum = this.biases.output[j];
            for (let i = 0; i < this.neurons; i++) {
                sum += hidden2[i] * this.weights.output[i][j];
            }
            output[j] = sum;
        }

        return this.softmax(output);
    }

    backward(state, prediction, targetAction) {
        // Simplified backpropagation for demonstration
        // In production, would use proper gradient descent
        
        const learningRate = this.learningRate;
        const target = new Array(4).fill(0);
        target[targetAction] = 1;

        // Update output layer
        for (let i = 0; i < this.neurons; i++) {
            for (let j = 0; j < 4; j++) {
                const error = target[j] - prediction[j];
                this.weights.output[i][j] += learningRate * error * 0.1;
            }
        }
    }

    predict(state) {
        if (!this.trained) {
            // Random action if not trained
            return Math.floor(Math.random() * 4);
        }

        const actionProbs = this.forward(state);
        return actionProbs.indexOf(Math.max(...actionProbs));
    }

    relu(x) {
        return Math.max(0, x);
    }

    softmax(arr) {
        const max = Math.max(...arr);
        const exp = arr.map(x => Math.exp(x - max));
        const sum = exp.reduce((a, b) => a + b, 0);
        return exp.map(x => x / sum);
    }

    crossEntropyLoss(prediction, target) {
        return -Math.log(prediction[target] + 1e-10);
    }

    shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    save() {
        return JSON.stringify({
            weights: this.weights,
            biases: this.biases,
            trained: this.trained
        });
    }

    load(modelData) {
        try {
            const data = JSON.parse(modelData);
            this.weights = data.weights;
            this.biases = data.biases;
            this.trained = data.trained;
            return true;
        } catch (e) {
            console.error('Failed to load model:', e);
            return false;
        }
    }
}

class DiffusionPolicyModel {
    constructor() {
        this.model = null;
        this.trained = false;
        this.diffusionSteps = 10;
        this.noiseSchedule = this.createNoiseSchedule(this.diffusionSteps);
        
        // Denoising network parameters
        this.denoisingNet = {
            weights1: this.initializeWeights(14, 32), // state(10) + action(4)
            weights2: this.initializeWeights(32, 32),
            weights3: this.initializeWeights(32, 4),
            biases1: new Array(32).fill(0),
            biases2: new Array(32).fill(0),
            biases3: new Array(4).fill(0)
        };
    }

    initializeWeights(inputSize, outputSize) {
        const weights = [];
        for (let i = 0; i < inputSize; i++) {
            weights[i] = [];
            for (let j = 0; j < outputSize; j++) {
                weights[i][j] = (Math.random() - 0.5) * 0.2;
            }
        }
        return weights;
    }

    createNoiseSchedule(steps) {
        // Linear noise schedule
        const schedule = [];
        for (let t = 0; t < steps; t++) {
            const beta = 0.0001 + (0.02 - 0.0001) * (t / steps);
            schedule.push(beta);
        }
        return schedule;
    }

    train(trainingData, epochs = 30) {
        console.log(`Training Diffusion Policy model on ${trainingData.states.length} samples...`);
        
        if (trainingData.states.length < 20) {
            console.warn('Not enough training data for diffusion policy. Need at least 20 samples.');
            return false;
        }

        for (let epoch = 0; epoch < epochs; epoch++) {
            let totalLoss = 0;

            for (let i = 0; i < trainingData.states.length; i++) {
                const state = trainingData.states[i];
                const action = trainingData.actions[i];
                
                // Random timestep
                const t = Math.floor(Math.random() * this.diffusionSteps);
                
                // Add noise to action
                const noisyAction = this.addNoise(this.oneHotEncode(action, 4), t);
                
                // Predict noise
                const predictedNoise = this.denoise(state, noisyAction, t);
                
                // Calculate loss (simplified)
                const noise = this.sampleNoise(4);
                const loss = this.mseLoss(predictedNoise, noise);
                totalLoss += loss;
                
                // Update weights (simplified gradient descent)
                this.updateWeights(state, noisyAction, predictedNoise, noise);
            }

            if (epoch % 5 === 0) {
                console.log(`Epoch ${epoch}: Loss = ${(totalLoss / trainingData.states.length).toFixed(4)}`);
            }
        }

        this.trained = true;
        console.log('Diffusion Policy model trained successfully!');
        return true;
    }

    denoise(state, noisyAction, timestep) {
        // Combine state, noisy action, and timestep
        const input = [...state, ...noisyAction, timestep / this.diffusionSteps];
        
        // Layer 1
        let hidden1 = new Array(32).fill(0);
        for (let j = 0; j < 32; j++) {
            let sum = this.denoisingNet.biases1[j];
            for (let i = 0; i < input.length; i++) {
                sum += input[i] * this.denoisingNet.weights1[i % this.denoisingNet.weights1.length][j];
            }
            hidden1[j] = this.tanh(sum);
        }

        // Layer 2
        let hidden2 = new Array(32).fill(0);
        for (let j = 0; j < 32; j++) {
            let sum = this.denoisingNet.biases2[j];
            for (let i = 0; i < 32; i++) {
                sum += hidden1[i] * this.denoisingNet.weights2[i][j];
            }
            hidden2[j] = this.tanh(sum);
        }

        // Output layer
        let output = new Array(4).fill(0);
        for (let j = 0; j < 4; j++) {
            let sum = this.denoisingNet.biases3[j];
            for (let i = 0; i < 32; i++) {
                sum += hidden2[i] * this.denoisingNet.weights3[i][j];
            }
            output[j] = sum;
        }

        return output;
    }

    sample(state) {
        if (!this.trained) {
            return Math.floor(Math.random() * 4);
        }

        // Start from pure noise
        let action = this.sampleNoise(4);

        // Iteratively denoise
        for (let t = this.diffusionSteps - 1; t >= 0; t--) {
            const predictedNoise = this.denoise(state, action, t);
            
            // Remove predicted noise
            const alpha = 1 - this.noiseSchedule[t];
            for (let i = 0; i < 4; i++) {
                action[i] = (action[i] - Math.sqrt(1 - alpha) * predictedNoise[i]) / Math.sqrt(alpha);
            }

            // Add noise for next step (except last)
            if (t > 0) {
                const noise = this.sampleNoise(4);
                const sigma = Math.sqrt(this.noiseSchedule[t]);
                for (let i = 0; i < 4; i++) {
                    action[i] += sigma * noise[i];
                }
            }
        }

        // Convert to discrete action
        return action.indexOf(Math.max(...action));
    }

    addNoise(action, timestep) {
        const noise = this.sampleNoise(action.length);
        const alpha = this.noiseSchedule[timestep];
        
        return action.map((a, i) => {
            return Math.sqrt(1 - alpha) * a + Math.sqrt(alpha) * noise[i];
        });
    }

    sampleNoise(size) {
        // Sample from standard normal distribution
        return Array.from({length: size}, () => this.randomNormal());
    }

    randomNormal() {
        // Box-Muller transform
        const u1 = Math.random();
        const u2 = Math.random();
        return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    }

    oneHotEncode(value, size) {
        const encoded = new Array(size).fill(0);
        encoded[value] = 1;
        return encoded;
    }

    mseLoss(pred, target) {
        let sum = 0;
        for (let i = 0; i < pred.length; i++) {
            sum += Math.pow(pred[i] - target[i], 2);
        }
        return sum / pred.length;
    }

    updateWeights(state, noisyAction, prediction, target) {
        // Simplified weight update
        const learningRate = 0.001;
        
        for (let i = 0; i < this.denoisingNet.weights3.length; i++) {
            for (let j = 0; j < this.denoisingNet.weights3[i].length; j++) {
                const error = target[j] - prediction[j];
                this.denoisingNet.weights3[i][j] += learningRate * error * 0.01;
            }
        }
    }

    tanh(x) {
        return Math.tanh(x);
    }

    save() {
        return JSON.stringify({
            denoisingNet: this.denoisingNet,
            trained: this.trained,
            noiseSchedule: this.noiseSchedule
        });
    }

    load(modelData) {
        try {
            const data = JSON.parse(modelData);
            this.denoisingNet = data.denoisingNet;
            this.trained = data.trained;
            this.noiseSchedule = data.noiseSchedule;
            return true;
        } catch (e) {
            console.error('Failed to load diffusion model:', e);
            return false;
        }
    }
}

// Model Manager
class MLModelManager {
    constructor() {
        this.imitationModel = new ImitationLearningModel();
        this.diffusionModel = new DiffusionPolicyModel();
        this.trainingInProgress = false;
    }

    async trainModels(gameplayData) {
        this.trainingInProgress = true;
        
        console.log('Starting ML model training...');
        console.log('Training data:', gameplayData.states.length, 'samples');

        // Train imitation learning model
        const ilSuccess = this.imitationModel.train(gameplayData, 50);
        
        // Train diffusion policy model
        const dpSuccess = this.diffusionModel.train(gameplayData, 30);

        this.trainingInProgress = false;

        return {
            imitationLearning: ilSuccess,
            diffusionPolicy: dpSuccess
        };
    }

    predictAction(state, modelType = 'imitation') {
        if (modelType === 'imitation') {
            return this.imitationModel.predict(state);
        } else if (modelType === 'diffusion') {
            return this.diffusionModel.sample(state);
        }
        return 0;
    }

    isModelTrained(modelType = 'imitation') {
        if (modelType === 'imitation') {
            return this.imitationModel.trained;
        } else if (modelType === 'diffusion') {
            return this.diffusionModel.trained;
        }
        return false;
    }

    saveModels() {
        return JSON.stringify({
            imitationModel: this.imitationModel.save(),
            diffusionModel: this.diffusionModel.save()
        });
    }

    loadModels(modelsData) {
        try {
            const data = JSON.parse(modelsData);
            this.imitationModel.load(data.imitationModel);
            this.diffusionModel.load(data.diffusionModel);
            return true;
        } catch (e) {
            console.error('Failed to load models:', e);
            return false;
        }
    }
}
