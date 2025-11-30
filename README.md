# 🌌 SolarForge: Procedural Fractal Solar System Explorer

SolarForge is a **3D procedural universe** rendered entirely on the GPU using **raymarching shaders**.  
Instead of hand-modeling planets and space scenes, the whole world is generated from **mathematical formulas** in real time.

Fly through an endless galaxy of **fractal solar systems**, orbit suns made of pure math, and watch nebulae morph as you move.  
This project is designed both as a **beautiful visual toy** and as a **learning lab** for building larger WebGL / shader projects.

---

## ✨ Concept

The idea comes from “procedural fractal worlds”:  
> A mathematical universe generated on the GPU using shaders.

But instead of a single endless cave or Menger sponge, SolarForge focuses on:

- **Solar systems** built from distance fields:
  - Stars, planets, moons, rings, asteroid belts.
- **Fractal details**:
  - Planet surfaces & craters created using layered noise.
  - Fractal nebula clouds in the background.
- **Infinite exploration**:
  - As you travel, seeds are generated from your coordinates to create new systems.
  - No level loading — the universe simply *emerges* as you move.

---

## 🔧 Tech Stack

- **Three.js** – Used for:
  - Camera, input handling, WebGL context, and a full-screen quad.
- **GLSL Fragment Shader (Raymarching)** – Used for:
  - Signed Distance Field (SDF) world
  - Lighting, shadows, reflections, and atmospheric effects.
- **JavaScript (ES Modules)** – Used for:
  - Game loop & state (camera, velocity, UI).
  - Procedural seed generation for each solar system.

No 3D models. No textures.  
**Everything is math.**

---

## 🎯 Learning Goals

This project is intentionally structured so it’s a good “big project” to learn from:

1. **Organized repo** for a serious WebGL app.
2. **Clear separation** between:
   - Rendering (shader)
   - Game logic (JS)
   - UI / controls.
3. **Shader pipeline**:
   - How to pass uniforms (camera position, time, etc.).
4. **Raymarching basics**:
   - Signed Distance Fields
   - Normal calculation
   - Soft shadows / ambient occlusion.
5. **Procedural generation**:
   - Using noise and hashing for infinite, repeatable worlds.

---

## 🚀 Features

- **Infinite Galaxy Navigation**
  - Fly freely through space.
  - Each “sector” spawns a new procedural solar system.
- **Fractal Stars & Planets**
  - Planets are built from SDF spheres + layered noise.
  - Fractal detail emerges as you get closer.
- **Dynamic Lighting**
  - Physically-inspired lighting from one or more suns.
  - Simple HDR tonemapping + bloom-style glow (in shader).
- **Atmospheric Effects**
  - Thin atmosphere shells around planets.
  - Color shifts based on sun direction & camera angle.
- **Nebula & Starfield Background**
  - Procedural noise-based nebula clouds.
  - Starfield generated from deterministic hash functions.
- **Exploration HUD (optional)**
  - On-screen info panel:
    - Current system seed
    - Nearest star/planet name
    - Distance from sun
    - FPS counter.

---

## 🕹 Controls (Default)

- `W / S` – Move forward / backward  
- `A / D` – Strafe left / right  
- `Q / E` – Move down / up  
- Mouse drag – Look around  
- `Shift` – Boost speed  
- `Space` – Toggle auto-orbit around nearest planet  
- `H` – Toggle HUD  
- `P` – Pause / unpause simulation

(You can adjust these in `src/controls.ts` or `controls.js` later.)

---

## 📁 Project Structure

```text
solarforge/
├── index.html           # Single-page app entry
├── src/
│   ├── main.js          # Bootstraps Three.js, renderer, and game loop
│   ├── scene.js         # Camera, uniforms, render loop wiring
│   ├── controls.js      # Keyboard / mouse controls
│   ├── ui.js            # HUD / overlay text
│   └── shaders/
│       └── solarforge.frag # Main raymarching fragment shader
├── assets/
│   └── fonts/           # Optional web fonts for UI
├── styles/
│   └── main.css         # Basic full-screen styling
├── package.json
└── README.md
