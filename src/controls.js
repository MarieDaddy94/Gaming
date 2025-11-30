import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

const KEYMAP = {
  KeyW: new THREE.Vector3(0, 0, -1),
  KeyS: new THREE.Vector3(0, 0, 1),
  KeyA: new THREE.Vector3(-1, 0, 0),
  KeyD: new THREE.Vector3(1, 0, 0),
  KeyQ: new THREE.Vector3(0, -1, 0),
  KeyE: new THREE.Vector3(0, 1, 0),
};

export function createControls(camera) {
  const velocity = new THREE.Vector3();
  const direction = new THREE.Vector3();
  const look = new THREE.Vector2();
  const pressed = new Set();
  let seed = 0;

  const sensitivity = 0.002;
  const baseSpeed = 6;
  const boost = 5;
  const drag = 0.95;

  camera.position.set(0, 1.5, 6);

  window.addEventListener('keydown', (event) => {
    pressed.add(event.code);
    if (event.code === 'Space') {
      seed = Math.floor((camera.position.length() + Date.now()) % 99999);
    }
  });

  window.addEventListener('keyup', (event) => {
    pressed.delete(event.code);
  });

  window.addEventListener('mousemove', (event) => {
    look.x -= event.movementX * sensitivity;
    look.y -= event.movementY * sensitivity;
  });

  function update(delta) {
    look.y = THREE.MathUtils.clamp(look.y, -Math.PI / 2 + 0.01, Math.PI / 2 - 0.01);
    camera.rotation.set(look.y, look.x, 0, 'YXZ');

    direction.set(0, 0, 0);
    pressed.forEach((code) => {
      const vector = KEYMAP[code];
      if (vector) {
        direction.add(vector);
      }
    });

    const accel = direction.length() > 0 ? direction.clone().normalize().applyEuler(camera.rotation) : direction;
    const speed = (pressed.has('ShiftLeft') || pressed.has('ShiftRight') ? baseSpeed * boost : baseSpeed) * delta;

    velocity.addScaledVector(accel, speed);
    velocity.multiplyScalar(drag);
    camera.position.add(velocity);
  }

  return {
    update,
    getSpeed: () => velocity.length(),
    getSeed: () => seed,
  };
}
