class Scene1 extends Phaser.Scene {
  constructor() {
    super("bootGame");
  }

  preload() {
    this.load.image("background", "images/background.png");
    this.load.image("ship", "images/ship.png");
    this.load.image("ship2", "images/ship2.png");
    this.load.image("ship3", "images/ship3.png");
  }

  create() {
    this.add.text(20, 20, "loading game.");
    this.scene.start("playGame");
  }
}
