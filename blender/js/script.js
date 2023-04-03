/**
 * Base
 */
// Canvas
const canvas = document.querySelector("canvas.webgl");

/**
 * Loaders
 */
const loadingBarElement = document.querySelector(".loading-bar");
const bodyElement = document.querySelector("body");
const loadingManager = new THREE.LoadingManager(
    () => {
        setTimeout(() => {
            gsap.to(overlayMaterial.uniforms.uAlpha, {
                duration: 3,
                value: 0,
                delay: 1,
            });
            gsap.to(overlayMaterial.uniforms.uAlpha, {
                duration: 3,
                value: 0,
                delay: 1,
            });

            loadingBarElement.classList.add("ended");
            bodyElement.classList.add("loaded");
            loadingBarElement.style.transform = "";
        }, 500);
    },
    (itemUrl, itemsLoaded, itemsTotal) => {
        const progressRatio = itemsLoaded / itemsTotal;
        loadingBarElement.style.transform = `scaleX(${progressRatio})`;
    },
    () => { }
);
const gltfLoader = new THREE.GLTFLoader(loadingManager);

/**
 *  Textures
 */
const textureLoader = new THREE.TextureLoader();
const alphaShadow = textureLoader.load("/assets/texture/simpleShadow.jpg");

// Scene
const scene = new THREE.Scene();

const sphereShadow = new THREE.Mesh(
    new THREE.PlaneGeometry(1, 1),
    new THREE.MeshBasicMaterial({
        transparent: true,
        color: 0x000000,
        opacity: 0.5,
        alphaMap: alphaShadow,
    })
);

sphereShadow.rotation.x = -Math.PI * 0.5;

sphereShadow.position.y = -1;
sphereShadow.position.x = 1;

scene.add(sphereShadow);

/**
 * Overlay
 */
const overlayGeometry = new THREE.PlaneGeometry(2, 2, 1, 1);
const overlayMaterial = new THREE.ShaderMaterial({
    vertexShader: `
        void main() {
            gl_Position = vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float uAlpha;
        void main() {
            gl_FragColor = vec4(0.0, 0.0, 0.0, uAlpha);
        }
    `,
    uniforms: {
        uAlpha: {
            value: 1.0,
        },
    },
    transparent: true,
});
const overlay = new THREE.Mesh(overlayGeometry, overlayMaterial);
scene.add(overlay);

/**
 * GLTF Model
 */
let car = null;

gltfLoader.load(
    "./assets/car/scene.gltf",
    (gltf) => {
        console.log(gltf);
        car = gltf.scene;

        const radius = 8.5;
        car.position.x = 20;
        car.rotation.y = -0.785398;
        car.scale.set(radius, radius, radius);

        scene.add(car);
    },
    (progress) => {
        console.log(progress);
    },
    (error) => {
        console.error(error);
    }
);

/**
 * Light
 */
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(1, 2, 0);
directionalLight.castShadow = true;
scene.add(directionalLight);

/**
 * Sizes
 */
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight,
};

/**
 * Scroll
 */
let scrollY = window.scrollY;
let currentSection = 0;

const transformcar = [
    {
        positionX: 20,
        rotationY: -0.785398,
    },
    {
        positionX: -20,
        rotationY: 2.79253,
    },
    {
        positionX: 0,
        rotationY: 0,
    },
];

window.addEventListener("scroll", () => {
    scrollY = window.scrollY;
    const newSection = Math.round(scrollY / sizes.height);

    console.log(newSection);

    if (newSection !== currentSection && !!car) {
        currentSection = newSection;

        gsap.to(car.rotation, {
            duration: 1.5,
            ease: "power2.inOut",
            y: transformcar[currentSection].rotationY,
        });

        gsap.to(car.position, {
            duration: 1.5,
            ease: "power2.inOut",
            x: transformcar[currentSection].positionX,
        });
    }
});

/**
 * Camera
 */
// Base camera
const camera = new THREE.PerspectiveCamera(
    35,
    sizes.width / sizes.height,
    0.1,
    1000
);
camera.position.z = 90;
scene.add(camera);

/**
 * Renderer
 */
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    alpha: true,
});
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

/**
 * Animate
 */
const clock = new THREE.Clock();
let lastElapsedTime = 0;

const tick = () => {
    const elapsedTime = clock.getElapsedTime();
    const deltaTime = elapsedTime - lastElapsedTime;
    lastElapsedTime = elapsedTime;

    if (!!car) {
        car.position.y = Math.sin(elapsedTime * 0.5) * 0.1 - 0.1;
        sphereShadow.material.opacity = (1 - Math.abs(car.position.y)) * 0.3;
    }

    // Render
    renderer.render(scene, camera);

    // Call tick again on the next frame
    window.requestAnimationFrame(tick);
};

tick();

/**
 * On Reload
 */
window.onbeforeunload = function () {
    window.scrollTo(0, 0);
};
