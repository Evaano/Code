import * as ex from "excalibur";
import { Hero } from "./src/actors/Hero/Hero.js";
import { MM_CameraStrategy } from "./src/classes/CameraStrategy.js";
import {
  CUSTOM_EVENT_CAMERA_Y_CHANGE,
  SCALE,
  SCALED_CELL,
  TAG_HERO,
} from "./src/constants.js";
import { Lifebar } from "./src/hud/Lifebar.js";
import { HeroHp } from "./src/classes/HeroHp.js";
import { DrewMan_Stage } from "./src/stages/DrewMan_Stage.js";
import { loader } from "./src/resources.js";

const game = new ex.Engine({
  width: 740 * SCALE,
  height: 370 * SCALE,
  fixedUpdateFps: 60,
  antialiasing: false, // Pixel art graphics
});

// Set global gravity
ex.Physics.acc = new ex.Vector(0, 1500);

// Global state classes
const mmHp = new HeroHp(game);

//-----------------------------------------------------------------------------------------

const stage = new DrewMan_Stage();
stage.rooms.forEach((room) => {
  game.add(room);
});

const hero = new Hero(45 * SCALED_CELL, 2 * SCALED_CELL);
game.add(hero);
const cameraStrategy = new MM_CameraStrategy(hero);
cameraStrategy.setRoomLimits(stage.firstMap.limits);

const lifebar = new Lifebar();
game.add(lifebar);

game.on("initialize", () => {
  game.currentScene.camera.addStrategy(cameraStrategy);
  game.currentScene.world.queryManager.createQuery([TAG_HERO]);
});

game.on(CUSTOM_EVENT_CAMERA_Y_CHANGE, async ({ yPos, direction, room }) => {
  // Change Y position
  cameraStrategy.onPinChange(yPos);
  cameraStrategy.setRoomLimits(room.limits);

  hero.setTransitioningRooms(direction);

  // Let the camera catch up
  await hero.actions.delay(1500).toPromise();

  hero.setTransitioningRooms(null);
});

await game.start(loader);

mmHp.init();
mmHp.hero = hero;
