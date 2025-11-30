const positionEl = document.getElementById('hud-position');
const velocityEl = document.getElementById('hud-velocity');
const seedEl = document.getElementById('hud-seed');
const fpsEl = document.getElementById('hud-fps');
const pointerLockEl = document.getElementById('hud-pointer-lock');

function formatNumber(value) {
  return value.toFixed(2);
}

export function createHud() {
  function update(pos, speed, seed, fps) {
    positionEl.textContent = `${formatNumber(pos.x)}, ${formatNumber(pos.y)}, ${formatNumber(pos.z)}`;
    velocityEl.textContent = `${formatNumber(speed)} u/s`;
    seedEl.textContent = `${seed}`;
    fpsEl.textContent = `${fps}`;
  }

  function setPointerLock(locked) {
    pointerLockEl.textContent = locked ? 'Locked' : 'Click canvas to capture mouse';
  }

  return { update, setPointerLock };
}
