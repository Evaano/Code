import * as ex from "excalibur";
import { Images } from "../../resources.js";

const heroSpriteSheet = ex.SpriteSheet.fromImageSource({
  image: Images.heroSheetImage,
  grid: {
    columns: 10,
    rows: 10,
    spriteWidth: 48,
    spriteHeight: 48,
  },
});

const idle = ex.Animation.fromSpriteSheet(heroSpriteSheet, [0], 200);
const idleRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [0], 200);
idleRight.flipHorizontal = true;

const idleShoot = ex.Animation.fromSpriteSheet(heroSpriteSheet, [10], 200);
const idleShootRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [10], 200);
idleShootRight.flipHorizontal = true;

const preStep = ex.Animation.fromSpriteSheet(heroSpriteSheet, [2], 200);
const preStepRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [2], 200);
preStepRight.flipHorizontal = true;

/* Individual runs here */
const run1 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [3], 200);
const run2 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [4], 200);
const run3 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [5], 200);

const runR1 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [3], 200);
runR1.flipHorizontal = true;
const runR2 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [4], 200);
runR2.flipHorizontal = true;
const runR3 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [5], 200);
runR3.flipHorizontal = true;

const runS1 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [13], 200);
const runS2 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [14], 200);
const runS3 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [15], 200);

const runRS1 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [13], 200);
runRS1.flipHorizontal = true;
const runRS2 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [14], 200);
runRS2.flipHorizontal = true;
const runRS3 = ex.Animation.fromSpriteSheet(heroSpriteSheet, [15], 200);
runRS3.flipHorizontal = true;

const pain = ex.Animation.fromSpriteSheet(heroSpriteSheet, [23], 200);
const painRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [23], 200);
painRight.flipHorizontal = true;

const jump = ex.Animation.fromSpriteSheet(heroSpriteSheet, [6], 200);
const jumpRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [6], 200);
jumpRight.flipHorizontal = true;

const jumpShoot = ex.Animation.fromSpriteSheet(heroSpriteSheet, [16], 200);
const jumpShootRight = ex.Animation.fromSpriteSheet(heroSpriteSheet, [16], 200);
jumpShootRight.flipHorizontal = true;

const ladder = ex.Animation.fromSpriteSheet(heroSpriteSheet, [20], 200);
const ladderR = ex.Animation.fromSpriteSheet(heroSpriteSheet, [21], 200);
const ladderShoot = ex.Animation.fromSpriteSheet(heroSpriteSheet, [31], 200);
const ladderShootR = ex.Animation.fromSpriteSheet(heroSpriteSheet, [31], 200);
ladderShootR.flipHorizontal = true;

const climbTop = ex.Animation.fromSpriteSheet(heroSpriteSheet, [22], 200);

const heroAnimations = {
  idle,
  idleRight,
  idleShoot,
  idleShootRight,
  preStep,
  preStepRight,
  run1,
  run2,
  run3,
  runR1,
  runR2,
  runR3,
  runS1,
  runS2,
  runS3,
  runRS1,
  runRS2,
  runRS3,
  pain,
  painRight,
  jump,
  jumpRight,
  jumpShoot,
  jumpShootRight,
  ladder,
  ladderR,
  ladderShoot,
  ladderShootR,
  climbTop,
};

export const animationMap = {
  IDLE: [idle, idleRight, idleShoot, idleShootRight],
  JUMP: [jump, jumpRight, jumpShoot, jumpShootRight],
  PRESTEP: [preStep, preStepRight, preStep, preStepRight],
  RUN1: [run1, runR1, runS1, runRS1],
  RUN2: [run2, runR2, runS2, runRS2],
  RUN3: [run3, runR3, runS3, runRS3],
  PAIN: [pain, painRight, pain, painRight],
  LADDER: [ladder, ladderR, ladderShoot, ladderShootR],
};

export default heroAnimations;
