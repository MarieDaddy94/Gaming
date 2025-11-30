import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import { createScene } from './scene.js';
import { createControls } from './controls.js';
import { createHud } from './ui.js';

const canvas = document.getElementById('app');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000000, 1);

const { scene, camera, uniforms } = createScene(renderer);
const hud = createHud();

const controls = createControls(camera, renderer.domElement, (locked) => {
  hud.setPointerLock(locked);
});
hud.setPointerLock(false);

let lastTime = performance.now();
let fpsTime = 0;
let fpsFrames = 0;

function resize() {
  const { innerWidth, innerHeight, devicePixelRatio } = window;
  renderer.setSize(innerWidth, innerHeight);
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  uniforms.uResolution.value.set(innerWidth * devicePixelRatio, innerHeight * devicePixelRatio);
}

function animate() {
  const now = performance.now();
  const delta = (now - lastTime) / 1000;
  lastTime = now;

  controls.update(delta);
  uniforms.uTime.value += delta;
  uniforms.uCameraPos.value.copy(camera.position);
  uniforms.uCameraMatrix.value.copy(camera.matrixWorld);
  uniforms.uSeed.value = controls.getSeed();

  renderer.render(scene, camera);

  fpsTime += delta;
  fpsFrames += 1;
  if (fpsTime >= 0.25) {
    const fps = Math.round(fpsFrames / fpsTime);
    const speed = controls.getSpeed();
    hud.update(camera.position, speed, controls.getSeed(), fps);
    fpsTime = 0;
    fpsFrames = 0;
  }

  requestAnimationFrame(animate);
}

window.addEventListener('resize', resize);
resize();
animate();
