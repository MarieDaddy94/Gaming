# 🌌 SolarForge: Procedural Fractal Solar System Explorer

SolarForge is a **3D procedural universe** rendered entirely on the GPU using **raymarching shaders**. Everything runs in the browser with no textures or models — just math.

---

## 🔥 Try it

1. Install dependencies (for the optional local dev server):
   ```bash
   npm install
   ```
2. Start a static server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000) and fly.

You can also open `index.html` directly in a modern browser.

---

## 🕹 Controls

- `W / S` – Move forward / backward
- `A / D` – Strafe left / right
- `Q / E` – Move down / up
- `Shift` – Boost speed
- `Mouse` – Look around
- `Space` – Generate a new seed (shifts nebula colors)

---

## 🧠 How it works

- **Three.js + ShaderMaterial** render a full-screen quad driven by a fragment shader.
- The fragment shader raymarches a tiny scene: a glowing star, a ringed planet, and layered nebula noise for the background.
- Camera orientation and position are passed to the shader each frame so rays originate from the player.
- A lightweight HUD overlays position, velocity, seed, and FPS to help with debugging the procedural world.

---

## 📁 Project Structure

```text
index.html            # Single-page app entry
styles/main.css       # Minimal UI styling
src/
  main.js             # Bootstraps renderer, game loop, and uniforms
  scene.js            # Shader-based scene setup
  controls.js         # Mouse + keyboard flight controls
  ui.js               # Heads-up display helpers
  shaders/
    solarforge.frag.js  # Raymarching fragment shader
package.json          # Dev server helper
```
