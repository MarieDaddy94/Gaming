import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import fragmentShader from './shaders/solarforge.frag.js';

export function createScene(renderer) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);

  const geometry = new THREE.PlaneGeometry(2, 2);
  const uniforms = {
    uTime: { value: 0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth * window.devicePixelRatio, window.innerHeight * window.devicePixelRatio) },
    uCameraPos: { value: new THREE.Vector3() },
    uCameraMatrix: { value: new THREE.Matrix4() },
    uSeed: { value: 0 },
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: /* glsl */ `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = vec4(position, 1.0);
      }
    `,
    fragmentShader,
  });

  const quad = new THREE.Mesh(geometry, material);
  quad.frustumCulled = false;
  scene.add(quad);

  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;

  return { scene, camera, uniforms };
}
