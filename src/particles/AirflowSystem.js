import { rand } from '../utils/math.js';

/**
 * Fresh air enters bottom (cyan), warm air leaves top (amber).
 * Full convection only in `airflow` mode.
 * `bottomOnly` shows weak bottom stir without sustained top exit — flame still fails.
 */
export class AirflowSystem {
  constructor() {
    this.inflow = [];
    this.outflow = [];
    this.bounds = null;
    this.mode = 'airflow';
  }

  update(dt, mode, bounds) {
    this.mode = mode;
    this.bounds = bounds;
    const full = mode === 'airflow';
    const bottomOnly = mode === 'bottomOnly';

    if (full || bottomOnly) {
      if (this.inflow.length < 28) {
        this.inflow.push(this._spawnIn(bounds));
      }
    } else {
      this.inflow.length = 0;
    }

    if (full) {
      if (this.outflow.length < 22) {
        this.outflow.push(this._spawnOut(bounds));
      }
    } else {
      this.outflow.length = 0;
    }

    for (const p of this.inflow) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt * 0.45;
      if (p.life <= 0) Object.assign(p, this._spawnIn(bounds));
    }
    for (const p of this.outflow) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt * 0.5;
      if (p.life <= 0) Object.assign(p, this._spawnOut(bounds));
    }
  }

  _spawnIn(b) {
    const side = Math.random() < 0.5 ? -1 : 1;
    return {
      x: b.cx + side * (b.w * 0.42),
      y: b.bottom - 6,
      vx: -side * rand(18, 36),
      vy: -rand(30, 70),
      life: rand(0.7, 1.4),
      r: rand(1.5, 3),
    };
  }

  _spawnOut(b) {
    return {
      x: b.cx + rand(-b.w * 0.25, b.w * 0.25),
      y: b.top + 8,
      vx: rand(-8, 8),
      vy: -rand(40, 80),
      life: rand(0.6, 1.2),
      r: rand(1.8, 3.4),
    };
  }

  draw(ctx) {
    if (!this.bounds) return;
    const b = this.bounds;

    // Labels
    if (this.mode === 'airflow') {
      ctx.fillStyle = 'rgba(158, 255, 240, 0.85)';
      ctx.font = '600 11px Sora, sans-serif';
      ctx.fillText('FRESH AIR ENTERS', b.x - 4, b.bottom + 22);
      ctx.fillStyle = 'rgba(255, 176, 112, 0.9)';
      ctx.fillText('WARM AIR LEAVES', b.x + 8, b.top - 14);
    }

    for (const p of this.inflow) {
      ctx.fillStyle = `rgba(158, 255, 240, ${0.55 * p.life})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
    for (const p of this.outflow) {
      ctx.fillStyle = `rgba(255, 176, 112, ${0.55 * p.life})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }

    // Arrow glyphs
    if (this.mode === 'airflow' || this.mode === 'bottomOnly') {
      this._arrow(ctx, b.cx - b.w * 0.55, b.bottom - 4, 18, -28, '#9efff0');
      this._arrow(ctx, b.cx + b.w * 0.55, b.bottom - 4, -18, -28, '#9efff0');
    }
    if (this.mode === 'airflow') {
      this._arrow(ctx, b.cx - 16, b.top + 4, 0, -36, '#ffb070');
      this._arrow(ctx, b.cx, b.top + 4, 0, -40, '#ffb070');
      this._arrow(ctx, b.cx + 16, b.top + 4, 0, -36, '#ffb070');
    }
  }

  _arrow(ctx, x, y, dx, dy, color) {
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 1.6;
    ctx.globalAlpha = 0.75;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + dx, y + dy);
    ctx.stroke();
    const ang = Math.atan2(dy, dx);
    ctx.beginPath();
    ctx.moveTo(x + dx, y + dy);
    ctx.lineTo(x + dx - Math.cos(ang - 0.4) * 8, y + dy - Math.sin(ang - 0.4) * 8);
    ctx.lineTo(x + dx - Math.cos(ang + 0.4) * 8, y + dy - Math.sin(ang + 0.4) * 8);
    ctx.closePath();
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}
