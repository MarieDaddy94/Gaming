export default /* glsl */ `
precision highp float;

uniform float uTime;
uniform vec2 uResolution;
uniform vec3 uCameraPos;
uniform mat4 uCameraMatrix;
uniform float uSeed;

varying vec2 vUv;

#define MAX_STEPS 128
#define MAX_DIST 120.0
#define SURF_DIST 0.001

vec3 hash33(vec3 p) {
  p = fract(p * vec3(0.1031, 0.11369, 0.13787) + uSeed * 0.0013);
  p += dot(p, p.yxz + 19.19);
  return -1.0 + 2.0 * fract(vec3((p.x + p.y) * p.z, (p.x + p.z) * p.y, (p.y + p.z) * p.x));
}

float hash11(float p) {
  p = fract(p * 0.1031 + uSeed * 0.0007);
  p *= p + 33.33;
  p *= p + p;
  return fract(p);
}

float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

float sdTorus(vec3 p, vec2 t) {
  vec2 q = vec2(length(p.xz) - t.x, p.y);
  return length(q) - t.y;
}

float fbm(vec3 p) {
  float f = 0.0;
  float a = 0.5;
  for (int i = 0; i < 5; i++) {
    f += a * sin(dot(p, vec3(1.2, 1.7, 1.4)));
    p *= 2.03;
    a *= 0.5;
    p += hash33(p) * 0.25;
  }
  return f;
}

float map(vec3 p, out int matId) {
  float star = sdSphere(p, 1.4);
  float glow = sdSphere(p, 1.6);

  vec3 planetPos = vec3(sin(uTime * 0.2 + uSeed * 0.3) * 6.0, 0.6 * sin(uTime * 0.17 + uSeed), cos(uTime * 0.2 + uSeed * 0.4) * 6.0);
  float planet = sdSphere(p - planetPos, 0.9 + 0.2 * sin(uTime * 0.6 + fbm(planetPos)));

  vec3 ringPos = p - planetPos;
  float ring = sdTorus(ringPos, vec2(1.8, 0.06));

  float nebula = 5.0 - length(p) + fbm(p * 0.05 + vec3(uTime * 0.02));

  float d = star;
  matId = 1;

  if (planet < d) {
    d = planet;
    matId = 2;
  }

  if (ring < d) {
    d = ring;
    matId = 3;
  }

  if (glow < d) {
    d = glow;
    matId = 4;
  }

  d = min(d, nebula);
  return d;
}

vec3 getNormal(vec3 p) {
  const vec2 e = vec2(0.001, 0.0);
  int m;
  float dx = map(p + vec3(e.x, e.y, e.y), m) - map(p - vec3(e.x, e.y, e.y), m);
  float dy = map(p + vec3(e.y, e.x, e.y), m) - map(p - vec3(e.y, e.x, e.y), m);
  float dz = map(p + vec3(e.y, e.y, e.x), m) - map(p - vec3(e.y, e.y, e.x), m);
  return normalize(vec3(dx, dy, dz));
}

vec3 shade(vec3 ro, vec3 rd) {
  float dist = 0.0;
  int matId = 0;
  for (int i = 0; i < MAX_STEPS; i++) {
    vec3 p = ro + rd * dist;
    float d = map(p, matId);
    dist += d;
    if (d < SURF_DIST || dist > MAX_DIST) break;
  }

  if (dist > MAX_DIST) {
    vec3 n = normalize(hash33(rd + uTime * 0.01));
    float starField = pow(max(0.0, dot(rd, n)), 12.0) * 1.5 + hash11(rd.x + rd.y + rd.z + uTime) * 0.02;
    return mix(vec3(0.02, 0.05, 0.08), vec3(0.09, 0.15, 0.25), starField + fbm(rd * 12.0) * 0.25);
  }

  vec3 p = ro + rd * dist;
  vec3 n = getNormal(p);
  vec3 lightPos = vec3(0.0, 0.0, 0.0);
  vec3 l = normalize(lightPos - p);
  float diff = clamp(dot(n, l), 0.0, 1.0);
  float spec = pow(max(dot(reflect(-l, n), -rd), 0.0), 32.0);
  float falloff = 2.0 / (1.0 + length(lightPos - p) * 0.25);

  vec3 col;
  if (matId == 1) {
    col = vec3(2.2, 1.6, 1.0) * falloff * 1.5;
  } else if (matId == 2) {
    float height = fbm(p * 3.0 + vec3(uTime * 0.2));
    col = mix(vec3(0.08, 0.15, 0.24), vec3(0.21, 0.42, 0.56), 0.5 + 0.5 * height);
    col += spec * 0.1;
  } else if (matId == 3) {
    col = vec3(0.8, 0.7, 0.4) * diff * 0.5 + vec3(0.02);
  } else {
    col = vec3(1.5, 0.8, 0.3) * falloff * 0.8;
  }

  vec3 glow = vec3(1.6, 1.0, 0.5) * exp(-dist * 0.06);
  col += glow * 0.1;
  col += spec * 0.15;
  col += 0.02 * fbm(p * 2.0) * vec3(0.3, 0.4, 0.6);
  col += 0.01 * pow(max(0.0, dot(rd, n)), 24.0);

  return pow(col, vec3(0.95));
}

vec3 getRayDirection(vec2 uv, vec3 camForward, vec3 camRight, vec3 camUp, float fov) {
  vec2 p = (uv - 0.5) * 2.0;
  p.x *= uResolution.x / uResolution.y;
  float z = 1.0 / tan(radians(fov) * 0.5);
  return normalize(camRight * p.x + camUp * p.y + camForward * z);
}

void main() {
  vec3 camPos = uCameraPos;
  vec3 camForward = normalize(vec3(uCameraMatrix[2].xyz * -1.0));
  vec3 camRight = normalize(vec3(uCameraMatrix[0].xyz));
  vec3 camUp = normalize(vec3(uCameraMatrix[1].xyz));

  vec3 rd = getRayDirection(vUv, camForward, camRight, camUp, 75.0);
  vec3 col = shade(camPos, rd);

  col = pow(col, vec3(0.9));
  col = col / (col + 1.0);

  gl_FragColor = vec4(col, 1.0);
}
`;
