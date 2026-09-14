import { prefersReducedMotion, particleBudget } from '../utils/math.js';

/** Soft floating atmosphere behind chapters */
export class Atmosphere {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.running = false;
    this.reduced = prefersReducedMotion();
    this._onResize = () => this.resize();
  }

  mount() {
    this.resize();
    const n = Math.min(40, particleBudget() / 2);
    this.particles = Array.from({ length: n }, () => ({
      x: Math.random() * this.w,
      y: Math.random() * this.h,
      r: 0.6 + Math.random() * 1.8,
      vx: -6 + Math.random() * 12,
      vy: -10 + Math.random() * 4,
      a: 0.08 + Math.random() * 0.18,
    }));
    window.addEventListener('resize', this._onResize);
    this.running = true;
    const loop = () => {
      if (!this.running) return;
      this.draw();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  unmount() {
    this.running = false;
    window.removeEventListener('resize', this._onResize);
  }

  resize() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    this.w = window.innerWidth;
    this.h = window.innerHeight;
    this.canvas.width = this.w * dpr;
    this.canvas.height = this.h * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  draw() {
    const { ctx, w, h } = this;
    ctx.clearRect(0, 0, w, h);
    if (this.reduced) return;
    for (const p of this.particles) {
      p.x += p.vx * 0.016;
      p.y += p.vy * 0.016;
      if (p.y < -10) p.y = h + 10;
      if (p.x < -10) p.x = w + 10;
      if (p.x > w + 10) p.x = -10;
      ctx.fillStyle = `rgba(94, 200, 255, ${p.a})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
