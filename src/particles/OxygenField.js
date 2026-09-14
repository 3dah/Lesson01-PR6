import { particleBudget, rand } from '../utils/math.js';

/** Cyan oxygen / air particles inside a region; density follows level 0..1 */
export class OxygenField {
  constructor() {
    this.particles = [];
    this.bounds = null;
    this._ensure(particleBudget());
  }

  _ensure(n) {
    while (this.particles.length < n) {
      this.particles.push(this._spawn(1));
    }
    if (this.particles.length > n) this.particles.length = n;
  }

  _spawn(level) {
    return {
      x: 0,
      y: 0,
      vx: rand(-8, 8),
      vy: rand(-12, -2),
      r: rand(1.2, 2.8),
      a: rand(0.25, 0.7),
      phase: rand(0, Math.PI * 2),
      alive: Math.random() < level,
    };
  }

  update(dt, level, bounds) {
    this.bounds = bounds;
    const budget = Math.floor(particleBudget() * (0.35 + level * 0.65));
    this._ensure(budget);

    const { x, y, w, h } = bounds;
    for (const p of this.particles) {
      if (Math.random() > level + 0.05) {
        p.alive = false;
        continue;
      }
      if (!p.alive && Math.random() < level * 0.08) {
        p.alive = true;
        p.x = x + rand(8, w - 8);
        p.y = y + rand(12, h - 20);
      }
      if (!p.alive) continue;

      p.phase += dt * 2;
      p.x += p.vx * dt;
      p.y += p.vy * dt + Math.sin(p.phase) * 4 * dt;
      if (p.x < x + 6 || p.x > x + w - 6) p.vx *= -1;
      if (p.y < y + 10 || p.y > y + h - 12) p.vy *= -1;
      p.x = Math.max(x + 6, Math.min(x + w - 6, p.x));
      p.y = Math.max(y + 10, Math.min(y + h - 12, p.y));
    }
  }

  draw(ctx, level) {
    if (!this.bounds) return;
    for (const p of this.particles) {
      if (!p.alive) continue;
      const alpha = p.a * (0.35 + level * 0.65);
      ctx.fillStyle = `rgba(122, 215, 255, ${alpha})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
