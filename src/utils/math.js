export function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

export function lerp(a, b, t) {
  return a + (b - a) * t;
}

export function rand(min, max) {
  return min + Math.random() * (max - min);
}

export function prefersReducedMotion() {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function particleBudget() {
  const cores = navigator.hardwareConcurrency || 4;
  const narrow = window.innerWidth < 700;
  if (narrow || cores <= 4) return 48;
  if (cores <= 8) return 90;
  return 130;
}
