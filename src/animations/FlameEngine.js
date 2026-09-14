/**
 * Procedural candle flame — strength 0..1 controls size/brightness.
 * strength → 0 extinguishes with residual smoke.
 */
export class FlameEngine {
  constructor(ctx, options = {}) {
    this.ctx = ctx;
    this.x = options.x ?? 0;
    this.y = options.y ?? 0;
    this.scale = options.scale ?? 1;
    this.strength = options.strength ?? 1;
    this.targetStrength = this.strength;
    this.time = 0;
    this.embers = [];
    this.smoke = [];
    this.alive = true;
  }

  setPosition(x, y, scale = this.scale) {
    this.x = x;
    this.y = y;
    this.scale = scale;
  }

  setStrength(v, immediate = false) {
    this.targetStrength = clamp01(v);
    if (immediate) this.strength = this.targetStrength;
    if (this.targetStrength <= 0.02) this._spawnExtinguish();
  }

  _spawnExtinguish() {
    for (let i = 0; i < 10; i++) {
      this.smoke.push({
        x: (Math.random() - 0.5) * 8,
        y: -Math.random() * 10,
        vx: (Math.random() - 0.5) * 0.4,
        vy: -0.4 - Math.random() * 0.6,
        life: 1,
        r: 4 + Math.random() * 8,
      });
    }
  }

  update(dt) {
    this.time += dt;
    this.strength += (this.targetStrength - this.strength) * Math.min(1, dt * 2.2);
    if (this.strength < 0.01) this.alive = false;

    for (const s of this.smoke) {
      s.x += s.vx;
      s.y += s.vy;
      s.life -= dt * 0.35;
      s.r += dt * 6;
    }
    this.smoke = this.smoke.filter((s) => s.life > 0);
  }

  draw() {
    const { ctx } = this;
    const s = this.strength;
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.scale(this.scale, this.scale);

    // glow
    if (s > 0.02) {
      const g = ctx.createRadialGradient(0, -18, 2, 0, -10, 70 * s);
      g.addColorStop(0, `rgba(255, 200, 80, ${0.35 * s})`);
      g.addColorStop(0.45, `rgba(255, 100, 30, ${0.12 * s})`);
      g.addColorStop(1, 'rgba(255, 60, 20, 0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(0, -12, 70 * s, 0, Math.PI * 2);
      ctx.fill();
    }

    if (s > 0.02) {
      this._drawFlameBody(s);
    }

    for (const sm of this.smoke) {
      ctx.fillStyle = `rgba(160, 170, 180, ${0.18 * sm.life})`;
      ctx.beginPath();
      ctx.arc(sm.x, sm.y - 20, sm.r, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  _drawFlameBody(s) {
    const { ctx, time } = this;
    const flicker = Math.sin(time * 11) * 0.04 + Math.sin(time * 17.3) * 0.03;
    const lean = Math.sin(time * 2.1) * 3 + Math.sin(time * 5.7) * 1.5;
    const h = 52 * s * (1 + flicker);
    const w = 18 * s * (1 - flicker * 0.5);

    ctx.save();
    ctx.translate(lean * 0.35, 0);

    // outer
    const outer = ctx.createLinearGradient(0, 0, 0, -h);
    outer.addColorStop(0, 'rgba(255, 90, 20, 0)');
    outer.addColorStop(0.15, `rgba(255, 90, 20, ${0.85 * s})`);
    outer.addColorStop(0.55, `rgba(255, 160, 40, ${0.95 * s})`);
    outer.addColorStop(1, `rgba(255, 230, 140, ${0.55 * s})`);
    ctx.fillStyle = outer;
    ctx.beginPath();
    ctx.moveTo(0, 2);
    ctx.bezierCurveTo(w, -h * 0.25, w * 0.7 + lean, -h * 0.65, lean * 0.2, -h);
    ctx.bezierCurveTo(-w * 0.55 + lean, -h * 0.65, -w, -h * 0.25, 0, 2);
    ctx.fill();

    // core
    const coreH = h * 0.62;
    const core = ctx.createLinearGradient(0, 0, 0, -coreH);
    core.addColorStop(0, 'rgba(255, 220, 120, 0)');
    core.addColorStop(0.3, `rgba(255, 230, 150, ${0.9 * s})`);
    core.addColorStop(1, `rgba(255, 255, 240, ${0.95 * s})`);
    ctx.fillStyle = core;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.bezierCurveTo(w * 0.35, -coreH * 0.3, w * 0.25, -coreH * 0.7, 0, -coreH);
    ctx.bezierCurveTo(-w * 0.25, -coreH * 0.7, -w * 0.35, -coreH * 0.3, 0, 0);
    ctx.fill();

    // wick tip
    ctx.strokeStyle = 'rgba(40, 28, 18, 0.85)';
    ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(0, 4);
    ctx.lineTo(0, -6 * s);
    ctx.stroke();

    ctx.restore();
  }
}

function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}
