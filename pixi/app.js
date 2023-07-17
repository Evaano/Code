// Import PIXI.js classes
const Application = PIXI.Application;
const AnimatedSprite = PIXI.AnimatedSprite;
const Container = PIXI.Container;

// Constants for gravity and jump force
const GRAVITY = 0.5;
const JUMP_FORCE = 15;

// Variables for jump state and vertical velocity
let isJumping = false;
let yVelocity = 0;

// Create a new PIXI application
const app = new Application({
    width: 1495,
    height: 760,
    transparent: false,
    antialias: false
});

// Set the background color and position of the renderer view
app.renderer.backgroundColor = 0x23395D;
app.renderer.view.style.position = 'absolute';

// Append the renderer view to the document body
document.body.appendChild(app.view);

// Create a PIXI loader
const loader = PIXI.Loader.shared;

// Load city texture and create a tiling sprite
const cityTexture = PIXI.Texture.from('./images/city.png');
const citySprite = new PIXI.TilingSprite(
    cityTexture,
    app.screen.width,
    app.screen.height
);

// Scale down the city sprite
citySprite.tileScale.set(0.5, 0.5);

// Add the city sprite to the stage
app.stage.addChild(citySprite);

// Create a new Howl sound instance
const sound = new Howl({
    src: ['./sound/pelimusaa.wav']
});

// Create a container to hold the animated sprites
const spriteContainer = new Container();
app.stage.addChild(spriteContainer);

// Load the spritesheets and set up animations
loader.add('spritesheet', './images/spritesheet.json').add('spritesheet2', './images/spritesheet2.json').load(setup);

let idleAnimation;
let runAnimation;
let currentAnimation;

// Function to set up animations
function setup(loader, resources) {
    // Frame names for idle and run animations
    const idleFrameNames = [
        'Idle1.png',
        'Idle2.png',
        'Idle3.png',
        'Idle4.png',
        'Idle5.png'
    ];

    const runFrameNames = [
        'Run1.png',
        'Run2.png',
        'Run3.png',
        'Run4.png',
        'Run5.png',
        'Run6.png',
        'Run7.png',
        'Run8.png'
    ];

    // Create animation frames from the loaded textures
    const idleFrames = idleFrameNames.map(frameName => resources.spritesheet.textures[frameName]);
    const runFrames = runFrameNames.map(frameName => resources.spritesheet2.textures[frameName]);

    // Create animated sprites for idle and run animations
    idleAnimation = new AnimatedSprite(idleFrames);
    runAnimation = new AnimatedSprite(runFrames);

    // Set initial positions and scales for the animations
    idleAnimation.position.set(600, 600);
    runAnimation.position.set(600, 600);
    idleAnimation.scale.set(2, 2);
    runAnimation.scale.set(2, 2);

    // Set animation speed and start playing the idle animation
    idleAnimation.animationSpeed = 0.050;
    runAnimation.animationSpeed = 0.050;
    idleAnimation.play();
    currentAnimation = idleAnimation;

    // Add the idle and run animations to the sprite container
    spriteContainer.addChild(idleAnimation);
    spriteContainer.addChild(runAnimation);

    // Set the initial visibility of the animations
    idleAnimation.visible = true;
    runAnimation.visible = false;

    // Add keyboard event listeners
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
}

const startText = new PIXI.Text('Press SPACE to Start Playing (*/ω＼*)', {
    fill: 0xffffff,
    fontSize: 36,
    fontFamily: 'Arial',
    fontWeight: 'bold'
});
startText.anchor.set(0.5);
startText.position.set(app.screen.width / 2, 100);
app.stage.addChild(startText);

// Function to hide the start text and start the game
function startGame() {
    startText.visible = false;
    // Add any other necessary logic to start the game
}

// Set to keep track of pressed keys
const keys = new Set();

// Event handler for keydown event
function handleKeyDown(event) {
    keys.add(event.code);

    // Start the game and hide the start text when Spacebar is pressed and the start text is visible
    if (keys.has('Space') && startText.visible) {
        startGame();
    }

    // Jump when the spacebar is pressed
    if (keys.has('Space') && !isJumping) {
        isJumping = true;
        yVelocity = -JUMP_FORCE;
    }

    updateBackground();
    updateAnimation();
}

// Event handler for keyup event
function handleKeyUp(event) {
    keys.delete(event.code);

    updateBackground();
    updateAnimation();
}

// Function to update the background position based on key inputs
function updateBackground() {
    if (keys.has('KeyA')) {
        citySprite.tilePosition.x += 3;
        runAnimation.scale.x = -2;
    }

    if (keys.has('KeyD')) {
        citySprite.tilePosition.x -= 3;
        runAnimation.scale.x = 2;
    }
}

// Function to update the current animation based on key inputs
function updateAnimation() {
    if (keys.has('KeyA') || keys.has('KeyD')) {
        if (currentAnimation !== runAnimation) {
            idleAnimation.visible = false;
            runAnimation.visible = true;
            runAnimation.play();
            currentAnimation = runAnimation;
        }
    } else {
        if (currentAnimation !== idleAnimation) {
            idleAnimation.visible = true;
            runAnimation.visible = false;

            // Check the direction of the previous run animation
            if (currentAnimation === runAnimation && runAnimation.scale.x === -2) {
                // If running left, use the mirrored idle animation
                idleAnimation.scale.x = -2;
            } else {
                // If running right or not running at all, use the normal idle animation
                idleAnimation.scale.x = 2;
            }

            // Reset the animation frame and play the idle animation
            idleAnimation.gotoAndPlay(0); // Use gotoAndPlay instead of gotoAndStop
            currentAnimation = idleAnimation;
        }
    }
}

// Function to update the game state
function update() {
    updateBackground();
    updateAnimation();

    if (isJumping) {
        // Apply gravity to the vertical velocity
        yVelocity += GRAVITY;
        spriteContainer.y += yVelocity;
        const FIXED_HEIGHT = 100;

        // Check if the sprite has landed on the ground
        if (spriteContainer.y >= FIXED_HEIGHT - spriteContainer.height) {
            // Set the sprite's position to the ground level
            spriteContainer.y = FIXED_HEIGHT - spriteContainer.height;
            isJumping = false;
            yVelocity = 0;

            updateBackground();
        }
    }
}

// Add the update function to the PIXI ticker
app.ticker.add(update);
