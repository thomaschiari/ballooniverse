Okay, this final version integrates **Balloon Theme Selection** and **Persistent Game State Saving** using `localStorage`, completing the feature set for *Ballooniverse*.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ballooniverse - Polished</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f0f0f0;
            font-family: 'Arial', sans-serif; /* Changed font slightly */
        }

        #game-container {
            position: relative;
            width: 400px;
            height: 600px;
            background: linear-gradient(to bottom, #87CEEB, #ADD8E6);
            border: 2px solid #333;
            overflow: hidden;
            cursor: default;
        }

        #world {
            position: relative;
            width: 100%;
            height: 100%;
            /* transform: translateY(0px); */ /* Updated by JS */
        }

        /* --- Balloon Base Styles (Positioning/Sizing) --- */
        #balloon {
            position: absolute;
            bottom: 50px;
            left: 175px;
            width: 50px;
            height: 70px;
            z-index: 10;
            /* Default appearance (will be overridden by themes) */
            background-color: #FF6347; /* Tomato red */
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            box-shadow: inset -5px -5px 10px rgba(0,0,0,0.2);
            transition: background-color 0.3s, border-radius 0.3s; /* Smooth theme transitions */
        }

        #balloon::after { /* String/basket */
            content: '';
            position: absolute;
            bottom: -10px;
            left: 20px;
            width: 10px;
            height: 15px;
            background-color: #8B4513;
            border-radius: 3px;
        }

        /* --- Balloon Theme Classes --- */
        .balloon-red { /* Default Theme */
            background-color: #FF6347; /* Tomato red */
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        }
        .balloon-blue {
            background-color: #4682B4; /* Steel blue */
            border-radius: 50%; /* More rounded */
        }
        .balloon-green-striped {
            background: repeating-linear-gradient(
                45deg,
                #90EE90, /* Light green */
                #90EE90 10px,
                #3CB371 10px, /* Medium sea green */
                #3CB371 20px
            );
            border-radius: 45% 55% 50% 50% / 60% 60% 40% 40%; /* Slightly irregular */
        }
        /* Add more themes here if desired */


        /* --- Obstacle Styles --- */
        .obstacle {
            position: absolute;
            background-color: #333;
            z-index: 5;
        }
        .obstacle.spike {
            width: 0; height: 0; /* Use borders for triangle */
            background-color: transparent;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-bottom: 40px solid #808080;
        }
         .obstacle.bar {
            width: 80px; height: 15px; background-color: #555; border-radius: 3px;
        }
         .obstacle.square {
             background-color: #A0522D; border: 1px solid #63351a;
         }
         .obstacle.bird {
            width: 35px; height: 25px; background-color: #ffeb3b;
            border-radius: 50% 50% 20% 20% / 60% 60% 40% 40%;
            border: 2px solid #c7b82e;
            box-shadow: inset 5px 5px 0px 0px #000; /* Eye */
            z-index: 6;
         }

        /* --- UI Screens & Overlays --- */
        .screen {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.65); /* Slightly darker overlay */
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; text-align: center; color: white; z-index: 20;
            padding: 20px; box-sizing: border-box;
        }
        .screen h2 { margin-bottom: 15px; font-size: 36px; text-shadow: 2px 2px 4px #000; }
        .screen p { font-size: 16px; margin-bottom: 20px; line-height: 1.4; }
        .screen button {
            padding: 12px 30px; font-size: 20px; cursor: pointer; border: none;
            border-radius: 5px; background-color: #4CAF50; color: white;
            transition: background-color 0.2s, transform 0.1s; margin-top: 10px;
        }
        .screen button:hover { background-color: #45a049; }
        .screen button:active { transform: scale(0.98); }

        #start-screen { display: flex; }
        #game-over-screen { display: none; }
        #pause-overlay { display: none; background-color: rgba(0, 0, 0, 0.75); }

        /* --- Theme Selection UI --- */
        #theme-selection {
            margin-top: 15px;
            margin-bottom: 25px;
        }
        #theme-selection h3 {
            margin-bottom: 10px;
            font-size: 18px;
            font-weight: normal;
        }
        .theme-options {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .theme-preview {
            width: 40px;
            height: 56px; /* Match aspect ratio */
            border: 3px solid transparent; /* For selection highlight */
            cursor: pointer;
            transition: border-color 0.2s, transform 0.2s;
            position: relative; /* For pseudo-elements if needed */
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .theme-preview:hover {
            transform: scale(1.1);
        }
        .theme-preview.selected {
            border-color: #fff; /* White border for selected */
            transform: scale(1.05); /* Slight scale up when selected */
        }
        /* Apply theme styles directly to previews */
        .theme-preview[data-theme="red"] { background-color: #FF6347; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; }
        .theme-preview[data-theme="blue"] { background-color: #4682B4; border-radius: 50%; }
        .theme-preview[data-theme="green-striped"] {
             background: repeating-linear-gradient(45deg, #90EE90, #90EE90 5px, #3CB371 5px, #3CB371 10px);
             border-radius: 45% 55% 50% 50% / 60% 60% 40% 40%;
        }

        /* --- Score Displays --- */
        #score { /* In-game score */
            position: absolute; top: 10px; left: 10px; font-size: 24px;
            color: #fff; text-shadow: 1px 1px 2px #000; z-index: 15;
        }
        #high-score-display { /* On start screen */
            margin-top: 5px;
            font-size: 16px;
            color: #eee;
        }
        #final-score { /* On game over screen */
             font-size: 20px; margin-bottom: 10px;
        }
         #game-over-high-score { /* High score on game over */
             font-size: 16px; color: #ffcc00; /* Gold color for high score */
             margin-bottom: 20px;
         }

    </style>
</head>
<body>

    <div id="game-container">
        <div id="score">Altitude: 0m</div>
        <div id="world"></div>
        <div id="balloon"></div> <!-- The actual game balloon -->

        <!-- UI Screens -->
        <div id="start-screen" class="screen">
            <h2>Ballooniverse</h2>
            <p>Float upwards and avoid the obstacles!<br>Use Arrow Keys or A/D to move. Press P to Pause.</p>

            <!-- Theme Selection Area -->
            <div id="theme-selection">
                <h3>Choose your Balloon:</h3>
                <div class="theme-options">
                    <div class="theme-preview" data-theme="red"></div>
                    <div class="theme-preview" data-theme="blue"></div>
                    <div class="theme-preview" data-theme="green-striped"></div>
                    <!-- Add more previews here -->
                </div>
            </div>

            <button id="play-button">Play</button>
            <p id="high-score-display">Highest Altitude: 0m</p>
        </div>

        <div id="game-over-screen" class="screen">
            <h2>Game Over!</h2>
            <p id="final-score">Final Altitude: 0m</p>
            <p id="game-over-high-score">Highest Altitude: 0m</p>
            <button id="restart-button">Restart</button>
        </div>

        <div id="pause-overlay" class="screen">
            <h2>Paused</h2>
            <p>Press P to Resume</p>
        </div>
    </div>

    <script>
        // --- DOM Elements ---
        const gameContainer = document.getElementById('game-container');
        const world = document.getElementById('world');
        const balloon = document.getElementById('balloon');
        const scoreDisplay = document.getElementById('score');
        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const pauseOverlay = document.getElementById('pause-overlay');
        const playButton = document.getElementById('play-button');
        const restartButton = document.getElementById('restart-button');
        const finalScoreDisplay = document.getElementById('final-score');
        const highScoreDisplayStart = document.getElementById('high-score-display');
        const highScoreDisplayGameOver = document.getElementById('game-over-high-score');
        const themeOptionsContainer = document.querySelector('.theme-options');
        const themePreviews = document.querySelectorAll('.theme-preview');

        // --- Game Constants ---
        const GAME_WIDTH = gameContainer.offsetWidth;
        const GAME_HEIGHT = gameContainer.offsetHeight;
        const BALLOON_WIDTH = 50; // Use fixed values as offsetWidth might not be ready initially
        const BALLOON_HEIGHT = 70;
        const BALLOON_MOVE_FORCE = 0.6;
        const BUOYANCY_FORCE = 0.04;
        const GRAVITY_FORCE = 0.015;
        const WIND_CHANGE_INTERVAL = 3000;
        const MAX_WIND_FORCE = 0.05;
        const HORIZONTAL_DAMPING = 0.95;
        const VERTICAL_DAMPING = 0.98;
        const CAMERA_THRESHOLD_Y = GAME_HEIGHT * 0.4;

        // --- Difficulty Scaling ---
        const INITIAL_OBSTACLE_SPEED = 2.5;
        const MAX_OBSTACLE_SPEED = 6;
        const INITIAL_SPAWN_INTERVAL = 1500;
        const MIN_SPAWN_INTERVAL = 500;
        const ALTITUDE_FOR_MAX_DIFFICULTY = 10000;

        // --- Bird AI Constants ---
        const BIRD_SPAWN_ALTITUDE_THRESHOLD = 500;
        const BIRD_TRACKING_SPEED_FACTOR = 0.03;
        const BIRD_BASE_VERTICAL_SPEED_MULTIPLIER = 1.1;

        // --- Local Storage Keys ---
        const LS_HIGH_SCORE_KEY = 'ballooniverse_highScore';
        const LS_SELECTED_THEME_KEY = 'ballooniverse_selectedTheme';

        // --- Game State ---
        let gameState = 'START';
        let balloonX, balloonY;
        let balloonVelocityX = 0;
        let balloonVelocityY = 0;
        let currentWindForceX = 0;
        let score = 0;
        let highScore = 0;
        let selectedTheme = 'red'; // Default theme
        let worldScrollY = 0;
        let obstacles = [];
        let gameLoopId = null;
        let obstacleSpawnIntervalId = null;
        let windChangeIntervalId = null;
        let keysPressed = {};

        // --- Audio ---
        let audioContext;
        let windSoundSource = null;
        let windGainNode = null;
        const WIND_VOLUME = 0.05;
        const POP_VOLUME = 0.3;

        // --- Utility Functions ---
        function lerp(a, b, t) { return a + (b - a) * t; }
        function random(min, max) { return Math.random() * (max - min) + min; }

        // --- Local Storage Handling ---
        function loadGameState() {
            try {
                const savedHighScore = localStorage.getItem(LS_HIGH_SCORE_KEY);
                const savedTheme = localStorage.getItem(LS_SELECTED_THEME_KEY);

                highScore = savedHighScore ? parseInt(savedHighScore, 10) : 0;
                selectedTheme = savedTheme || 'red'; // Default to 'red' if nothing saved

            } catch (e) {
                console.error("Could not load game state from localStorage:", e);
                highScore = 0;
                selectedTheme = 'red';
            }
            // Update UI elements that depend on loaded state
            highScoreDisplayStart.textContent = `Highest Altitude: ${highScore}m`;
            highScoreDisplayGameOver.textContent = `Highest Altitude: ${highScore}m`; // Also update on game over screen
            applyBalloonTheme(selectedTheme);
            updateThemeSelectionUI(selectedTheme);
        }

        function saveGameState() {
            try {
                // Update high score if current score is higher
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem(LS_HIGH_SCORE_KEY, highScore.toString());
                    // Update displays immediately if game over screen is visible
                     if (gameState === 'GAME_OVER') {
                         highScoreDisplayGameOver.textContent = `Highest Altitude: ${highScore}m`;
                     }
                }
                // Save the currently selected theme
                localStorage.setItem(LS_SELECTED_THEME_KEY, selectedTheme);

            } catch (e) {
                console.error("Could not save game state to localStorage:", e);
            }
        }

        // --- Theme Handling ---
        function applyBalloonTheme(themeName) {
            // Remove existing theme classes
            balloon.classList.remove('balloon-red', 'balloon-blue', 'balloon-green-striped'); // Add any other theme classes here
            // Add the new theme class
            balloon.classList.add(`balloon-${themeName}`);
        }

        function updateThemeSelectionUI(themeName) {
            themePreviews.forEach(preview => {
                if (preview.dataset.theme === themeName) {
                    preview.classList.add('selected');
                } else {
                    preview.classList.remove('selected');
                }
            });
        }

        function handleThemeSelection(event) {
            const target = event.target;
            if (target.classList.contains('theme-preview') && target.dataset.theme) {
                selectedTheme = target.dataset.theme;
                applyBalloonTheme(selectedTheme); // Update the main balloon's appearance immediately
                updateThemeSelectionUI(selectedTheme);
                // Note: We don't save to localStorage here, only on game over.
            }
        }


        // --- Audio Initialization and Control ---
        function initAudio() {
            if (!audioContext) {
                try {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                     // Resume context if suspended, often needed after user interaction
                     if (audioContext.state === 'suspended') {
                         audioContext.resume().catch(e => console.error("Audio context resume failed:", e));
                     }
                } catch (e) {
                    console.error("Web Audio API is not supported:", e);
                    return;
                }
            }
             // Double check state after creation/resume attempt
             if (audioContext && audioContext.state === 'suspended') {
                 console.warn("AudioContext is suspended. Waiting for user interaction.");
                 // Add a one-time interaction listener to resume context
                 const resumeAudio = () => {
                     if (audioContext.state === 'suspended') {
                         audioContext.resume().then(() => {
                             console.log("AudioContext resumed on interaction.");
                             // Now try creating/playing sounds again if needed
                             if (gameState === 'PLAYING' && !windSoundSource) {
                                 createWindSound();
                                 playWind();
                             }
                         }).catch(e => console.error("Audio context resume failed on interaction:", e));
                     }
                     document.body.removeEventListener('click', resumeAudio, true); // Clean up listener
                 };
                 document.body.addEventListener('click', resumeAudio, { once: true, capture: true });
             }
        }

        function createWindSound() {
            if (!audioContext || audioContext.state !== 'running') return; // Don't create if context not ready
            stopWind();

            windSoundSource = audioContext.createBufferSource();
            windGainNode = audioContext.createGain();
            const bufferSize = audioContext.sampleRate * 2;
            const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
            const output = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) output[i] = Math.random() * 2 - 1;
            windSoundSource.buffer = buffer;
            windSoundSource.loop = true;
            const filter = audioContext.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.setValueAtTime(400, audioContext.currentTime);
            windGainNode.gain.setValueAtTime(0, audioContext.currentTime);
            windSoundSource.connect(filter);
            filter.connect(windGainNode);
            windGainNode.connect(audioContext.destination);
        }

        function playWind() {
            if (!windSoundSource || !windGainNode || audioContext.state !== 'running') {
                 // Attempt to create if missing and context is running
                 if (audioContext && audioContext.state === 'running') {
                     createWindSound();
                     if (!windSoundSource) return; // Still failed
                 } else {
                     return; // Context not ready
                 }
            }
            try {
                 windSoundSource.start(0);
                 windGainNode.gain.linearRampToValueAtTime(WIND_VOLUME, audioContext.currentTime + 0.5);
            } catch(e) {
                 // Handle potential error if source was already started (e.g., rapid pause/resume)
                 console.warn("Could not start wind sound, possibly already playing.", e);
                 // Ensure gain is correct if already playing
                 windGainNode.gain.linearRampToValueAtTime(WIND_VOLUME, audioContext.currentTime + 0.5);
            }
        }

        function pauseWind() {
            if (windGainNode && audioContext && audioContext.state === 'running') {
                windGainNode.gain.linearRampToValueAtTime(0.0001, audioContext.currentTime + 0.2); // Fade almost to zero
            }
        }
        function resumeWind() {
             if (windGainNode && audioContext && audioContext.state === 'running') {
                 windGainNode.gain.linearRampToValueAtTime(WIND_VOLUME, audioContext.currentTime + 0.2);
             } else if (audioContext && audioContext.state === 'running') {
                 // If gain node was lost somehow, try recreating and playing
                 playWind();
             }
        }
        function stopWind() {
            if (windSoundSource) {
                try { windSoundSource.stop(); } catch (e) {}
                windSoundSource.disconnect(); windSoundSource = null;
            }
            if (windGainNode) { windGainNode.disconnect(); windGainNode = null; }
        }

        function playPopSound() {
            if (!audioContext || audioContext.state !== 'running') return;
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            oscillator.type = 'triangle';
            oscillator.frequency.setValueAtTime(880, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(110, audioContext.currentTime + 0.1);
            gainNode.gain.setValueAtTime(POP_VOLUME, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.15);
            oscillator.connect(gainNode); gainNode.connect(audioContext.destination);
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.15);
        }


        // --- Initialization ---
        function init() {
            gameState = 'START';
            balloonX = (GAME_WIDTH - BALLOON_WIDTH) / 2;
            balloonY = 50;
            balloonVelocityX = 0; balloonVelocityY = 0;
            currentWindForceX = 0;
            score = 0; // Reset score for the new game
            worldScrollY = 0;
            keysPressed = {};

            obstacles.forEach(obstacle => obstacle.element.remove());
            obstacles = [];

            // Load high score and theme preference *before* setting initial UI
            loadGameState(); // This now sets highScore and selectedTheme, and applies theme

            // Reset visual elements
            balloon.style.left = `${balloonX}px`;
            balloon.style.bottom = `${balloonY}px`; // Position balloon correctly even on start screen
            world.style.transform = `translateY(0px)`;
            scoreDisplay.textContent = `Altitude: 0m`; // Reset in-game score display

            // Setup UI screens
            gameOverScreen.style.display = 'none';
            pauseOverlay.style.display = 'none';
            startScreen.style.display = 'flex';

            // Clear intervals/loops
            if (gameLoopId) cancelAnimationFrame(gameLoopId); gameLoopId = null;
            if (obstacleSpawnIntervalId) clearInterval(obstacleSpawnIntervalId); obstacleSpawnIntervalId = null;
            if (windChangeIntervalId) clearInterval(windChangeIntervalId); windChangeIntervalId = null;

            // Remove old listeners
            document.removeEventListener('keydown', handleKeyDown);
            document.removeEventListener('keyup', handleKeyUp);
            restartButton.removeEventListener('click', init);
            playButton.removeEventListener('click', startGame); // Remove previous listener if any
            themeOptionsContainer.removeEventListener('click', handleThemeSelection);

            // Stop sounds
            stopWind();

            // Add listeners for start screen
            playButton.addEventListener('click', startGame, { once: true });
            themeOptionsContainer.addEventListener('click', handleThemeSelection);
            restartButton.addEventListener('click', init, { once: true }); // Re-add restart listener

            // Attempt to initialize audio context early
            initAudio();
        }

        // --- Game Start ---
        function startGame() {
            // Ensure audio context is ready (might need interaction)
            initAudio(); // Call again to handle potential suspension

            gameState = 'PLAYING';
            startScreen.style.display = 'none';

            // Apply the selected theme definitively one last time
            applyBalloonTheme(selectedTheme);

            // Start sounds if context is ready
            if (audioContext && audioContext.state === 'running') {
                 createWindSound(); // Create fresh source
                 playWind();
            } else {
                 console.warn("Cannot play wind sound: AudioContext not running.");
            }

            // Add game event listeners
            document.addEventListener('keydown', handleKeyDown);
            document.addEventListener('keyup', handleKeyUp);

            // Start game loops
            gameLoopId = requestAnimationFrame(gameLoop);
            startObstacleSpawning();
            windChangeIntervalId = setInterval(updateWind, WIND_CHANGE_INTERVAL);
        }

        // --- Input Handling ---
        function handleKeyDown(event) {
            const key = event.key.toLowerCase();
             if (gameState === 'PLAYING') keysPressed[key] = true;
             if (key === 'p') togglePause();
        }
        function handleKeyUp(event) { keysPressed[event.key.toLowerCase()] = false; }

        // --- Pause / Resume ---
        function togglePause() {
            if (gameState === 'PLAYING') {
                gameState = 'PAUSED';
                pauseOverlay.style.display = 'flex';
                clearInterval(obstacleSpawnIntervalId); obstacleSpawnIntervalId = null;
                clearInterval(windChangeIntervalId); windChangeIntervalId = null;
                pauseWind();
            } else if (gameState === 'PAUSED') {
                gameState = 'PLAYING';
                pauseOverlay.style.display = 'none';
                // Resume audio first (might need interaction state)
                resumeWind();
                // Resume game logic
                startObstacleSpawning();
                windChangeIntervalId = setInterval(updateWind, WIND_CHANGE_INTERVAL);
                gameLoopId = requestAnimationFrame(gameLoop);
            }
        }

        // --- Physics and Movement ---
        function applyForces() { /* ... (no changes needed) ... */
            balloonVelocityY += BUOYANCY_FORCE - GRAVITY_FORCE;
            balloonVelocityX += currentWindForceX;
            if (keysPressed['arrowleft'] || keysPressed['a']) balloonVelocityX -= BALLOON_MOVE_FORCE;
            if (keysPressed['arrowright'] || keysPressed['d']) balloonVelocityX += BALLOON_MOVE_FORCE;
            balloonVelocityX *= HORIZONTAL_DAMPING;
            balloonVelocityY *= VERTICAL_DAMPING;
        }
        function updateBalloonPosition() { /* ... (no changes needed) ... */
            balloonX += balloonVelocityX;
            balloonY += balloonVelocityY;
            if (balloonX < 0) { balloonX = 0; balloonVelocityX = 0; }
            if (balloonX > GAME_WIDTH - BALLOON_WIDTH) { balloonX = GAME_WIDTH - BALLOON_WIDTH; balloonVelocityX = 0; }
            if (balloonY < 0) { balloonY = 0; balloonVelocityY = Math.max(0, balloonVelocityY); }
            if (balloonY > CAMERA_THRESHOLD_Y) {
                const scrollAmount = balloonY - CAMERA_THRESHOLD_Y;
                worldScrollY += scrollAmount;
                balloonY = CAMERA_THRESHOLD_Y;
                world.style.transform = `translateY(-${worldScrollY}px)`;
                score = Math.floor(worldScrollY); // Update score based on scroll
                updateScoreDisplay();
            }
            balloon.style.left = `${balloonX}px`;
            balloon.style.bottom = `${balloonY}px`;
        }
        function updateWind() { /* ... (no changes needed) ... */
             if (gameState !== 'PLAYING') return;
             currentWindForceX = random(-MAX_WIND_FORCE, MAX_WIND_FORCE);
        }

        // --- Obstacle Management ---
        function getDifficultyFactor() { return Math.min(1, score / ALTITUDE_FOR_MAX_DIFFICULTY); }
        function getCurrentObstacleSpeed() { return lerp(INITIAL_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED, getDifficultyFactor()); }
        function getCurrentSpawnInterval() { return lerp(INITIAL_SPAWN_INTERVAL, MIN_SPAWN_INTERVAL, getDifficultyFactor()); }
        function startObstacleSpawning() { /* ... (no changes needed) ... */
             if (obstacleSpawnIntervalId) clearInterval(obstacleSpawnIntervalId);
             const interval = getCurrentSpawnInterval();
             obstacleSpawnIntervalId = setInterval(createObstacle, interval);
        }
        function createObstacle() { /* ... (no changes needed) ... */
            if (gameState !== 'PLAYING') return;
            const obstacleElement = document.createElement('div');
            obstacleElement.classList.add('obstacle');
            const obstacleType = Math.random();
            let obstacleWidth, obstacleHeight, obstacleClass = '', isBird = false;
            let baseSpeed = getCurrentObstacleSpeed(); let obstacleSpeed = baseSpeed;
            if (obstacleType < 0.5) { // Bar
                 obstacleWidth = random(50, 100); obstacleHeight = random(15, 25); obstacleClass = 'bar';
                 obstacleElement.style.backgroundColor = '#555';
            } else if (obstacleType < 0.75) { // Spike
                 obstacleWidth = 20; obstacleHeight = 40; obstacleClass = 'spike';
                 // CSS handles appearance
            } else if (obstacleType < 0.9 && score > BIRD_SPAWN_ALTITUDE_THRESHOLD) { // Bird
                 obstacleWidth = 35; obstacleHeight = 25; obstacleClass = 'bird'; isBird = true;
                 obstacleSpeed = baseSpeed * BIRD_BASE_VERTICAL_SPEED_MULTIPLIER;
                 // CSS handles appearance
            } else { // Square
                 obstacleWidth = random(25, 40); obstacleHeight = obstacleWidth; obstacleClass = 'square';
                 obstacleElement.style.backgroundColor = '#A0522D';
            }
            obstacleElement.style.width = `${obstacleWidth}px`;
            obstacleElement.style.height = `${obstacleHeight}px`;
            if (obstacleClass) obstacleElement.classList.add(obstacleClass);
            const maxLeft = GAME_WIDTH - obstacleWidth;
            const randomLeft = Math.random() * maxLeft;
            obstacleElement.style.left = `${randomLeft}px`;
            const spawnY = worldScrollY - obstacleHeight - random(50, 150);
            obstacleElement.style.top = `${spawnY}px`;
            world.appendChild(obstacleElement);
            obstacles.push({ element: obstacleElement, x: randomLeft, y: spawnY, width: obstacleWidth, height: obstacleHeight, speed: obstacleSpeed, isBird: isBird, tracking: isBird });
        }
        function moveObstacles() { /* ... (no changes needed) ... */
            const balloonBottomInWorld = worldScrollY + (GAME_HEIGHT - balloonY - BALLOON_HEIGHT);
            for (let i = obstacles.length - 1; i >= 0; i--) {
                const obstacle = obstacles[i];
                if (obstacle.isBird && obstacle.tracking) {
                    const targetX = balloonX + BALLOON_WIDTH / 2 - obstacle.width / 2;
                    const dx = targetX - obstacle.x;
                    obstacle.x += dx * BIRD_TRACKING_SPEED_FACTOR;
                    obstacle.x = Math.max(0, Math.min(GAME_WIDTH - obstacle.width, obstacle.x));
                    obstacle.element.style.left = `${obstacle.x}px`;
                    if (obstacle.y > balloonBottomInWorld) obstacle.tracking = false;
                }
                obstacle.y += obstacle.speed;
                obstacle.element.style.top = `${obstacle.y}px`;
                if (obstacle.y > worldScrollY + GAME_HEIGHT + 50) {
                    obstacle.element.remove(); obstacles.splice(i, 1);
                }
            }
        }

        // --- Collision Detection ---
        function checkCollision() { /* ... (no changes needed) ... */
            const balloonRect = balloon.getBoundingClientRect();
            obstacles.forEach(obstacle => {
                const obstacleRect = obstacle.element.getBoundingClientRect();
                if ( balloonRect.left < obstacleRect.right && balloonRect.right > obstacleRect.left &&
                     balloonRect.top < obstacleRect.bottom && balloonRect.bottom > obstacleRect.top ) {
                    gameOver();
                }
            });
        }

        // --- Scoring ---
        function updateScoreDisplay() { /* ... (no changes needed) ... */
            scoreDisplay.textContent = `Altitude: ${score}m`;
        }

        // --- Game State Management ---
        function gameOver() {
            if (gameState === 'GAME_OVER') return;
            gameState = 'GAME_OVER';

            playPopSound();
            stopWind();

            cancelAnimationFrame(gameLoopId); gameLoopId = null;
            clearInterval(obstacleSpawnIntervalId); obstacleSpawnIntervalId = null;
            clearInterval(windChangeIntervalId); windChangeIntervalId = null;

            document.removeEventListener('keydown', handleKeyDown);
            document.removeEventListener('keyup', handleKeyUp);

            // Save score and theme *before* displaying game over screen
            saveGameState(); // This updates highScore if needed and saves theme

            // Update Game Over screen displays
            finalScoreDisplay.textContent = `Final Altitude: ${score}m`;
            highScoreDisplayGameOver.textContent = `Highest Altitude: ${highScore}m`; // Ensure this shows the potentially updated high score
            gameOverScreen.style.display = 'flex';

            // Listener for restart is added in init() now
        }

        // --- Main Game Loop ---
        function gameLoop() { /* ... (no changes needed, dynamic interval adjustment removed for simplicity) ... */
            if (gameState === 'PAUSED') {
                 gameLoopId = requestAnimationFrame(gameLoop); return;
            }
            if (gameState !== 'PLAYING') return;

            applyForces();
            updateBalloonPosition();
            moveObstacles();
            checkCollision();

            // Removed dynamic interval adjustment here for stability.
            // Interval is set on start and pause/resume based on current score.

            if (gameState === 'PLAYING') {
                 gameLoopId = requestAnimationFrame(gameLoop);
            }
        }

        // --- Initial Setup ---
        init(); // Start the initialization process

    </script>

</body>
</html>
```

**Key Additions and Changes:**

1.  **Theme Selection (HTML/CSS):**
    *   Added a `#theme-selection` section within the `#start-screen`.
    *   Included `.theme-preview` divs with `data-theme` attributes.
    *   Added CSS rules for `.balloon-red`, `.balloon-blue`, `.balloon-green-striped` to style both the main balloon (`#balloon`) and the previews.
    *   Added `.selected` class styling for the chosen preview.
2.  **Theme Selection (JavaScript):**
    *   `selectedTheme` variable tracks the choice.
    *   `applyBalloonTheme(themeName)` function updates the `#balloon` element's class.
    *   `updateThemeSelectionUI(themeName)` highlights the correct preview.
    *   `handleThemeSelection(event)` listens for clicks on previews, updates `selectedTheme`, and calls the UI update functions.
    *   The selected theme is loaded in `loadGameState` and applied in `init`. It's reapplied definitively in `startGame`.
3.  **Save/Load Game State (JavaScript):**
    *   Defined `LS_HIGH_SCORE_KEY` and `LS_SELECTED_THEME_KEY` constants.
    *   `loadGameState()`: Reads `highScore` and `selectedTheme` from `localStorage` (with defaults) and updates relevant variables and UI elements (`highScoreDisplayStart`, `highScoreDisplayGameOver`, applies theme). Called during `init`.
    *   `saveGameState()`: Compares current `score` with `highScore`, updates `highScore` if needed, and saves both `highScore` and `selectedTheme` to `localStorage`. Called during `gameOver`.
    *   Used `try...catch` blocks for robustness around `localStorage` access.
4.  **UI Updates:**
    *   Added `#high-score-display` to the start screen.
    *   Added `#game-over-high-score` to the game over screen. Both are updated by `loadGameState` and potentially by `saveGameState` if the game over screen is active when a new high score is set.
5.  **Audio Context Handling:** Improved `initAudio` to better handle suspended states and user interaction requirements for resuming the context.
6.  **Initialization Flow:** `init()` now calls `loadGameState()` early to ensure saved preferences are applied before the start screen is fully set up. Event listeners are carefully added and removed to prevent duplicates across restarts.

*Ballooniverse* is now feature-complete with customization and persistence! Players can choose their look, and their achievements are remembered across sessions.