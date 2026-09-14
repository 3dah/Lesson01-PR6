import { FlameEngine } from './FlameEngine.js';
import { OxygenField } from '../particles/OxygenField.js';
import { AirflowSystem } from '../particles/AirflowSystem.js';
import { prefersReducedMotion } from '../utils/math.js';

/**
 * Interactive experiment apparatus + flame + air visualization.
 * Modes: free | openTop | sealed | bottomOnly | airflow
 */
export class ExperimentRig {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.mode = 'free';
    this.buildStep = 5; // 0..5 how much apparatus is shown
    this.showOxygen = false;
    this.showAirflow = false;
    this.oxygenLevel = 1;
    this.flame = new FlameEngine(this.ctx, { strength: 1 });
    this.oxygen = new OxygenField();
    this.airflow = new AirflowSystem();
    this.raf = 0;
    this.last = 0;
    this.running = false;
    this.reduced = prefersReducedMotion();
    this._onResize = () => this.resize();
  }

  mount() {
    this.resize();
    window.addEventListener('resize', this._onResize);
    this.running = true;
    this.last = performance.now();
    const loop = (now) => {
      if (!this.running) return;
      const dt = Math.min(0.05, (now - this.last) / 1000);
      this.last = now;
      this.update(dt);
      this.draw();
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  unmount() {
    this.running = false;
    cancelAnimationFrame(this.raf);
    window.removeEventListener('resize', this._onResize);
  }

  resize() {
    const rect = this.canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.w = Math.max(1, rect.width);
    this.h = Math.max(1, rect.height);
    this.canvas.width = Math.floor(this.w * dpr);
    this.canvas.height = Math.floor(this.h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  setMode(mode) {
    this.mode = mode;
    if (mode === 'sealed') {
      this.showOxygen = true;
      this.showAirflow = false;
    } else if (mode === 'airflow') {
      this.showOxygen = true;
      this.showAirflow = true;
      this.oxygenLevel = 1;
      this.flame.setStrength(1);
    } else if (mode === 'bottomOnly') {
      this.showOxygen = true;
      this.showAirflow = true;
    } else if (mode === 'openTop') {
      this.showOxygen = true;
      this.showAirflow = false;
      this.oxygenLevel = 1;
      this.flame.setStrength(1);
    } else {
      this.showAirflow = false;
    }
  }

  setBuildStep(step) {
    this.buildStep = step;
  }

  setOxygenLevel(v) {
    this.oxygenLevel = Math.max(0, Math.min(1, v));
    this.flame.setStrength(this.oxygenLevel > 0.08 ? 0.25 + this.oxygenLevel * 0.75 : 0);
  }

  /** Animate sealed jar depletion */
  deplete(duration = 4.5) {
    return new Promise((resolve) => {
      const start = performance.now();
      const from = this.oxygenLevel;
      const tick = (now) => {
        const t = Math.min(1, (now - start) / (duration * 1000));
        const eased = 1 - Math.pow(1 - t, 2);
        this.setOxygenLevel(from * (1 - eased));
        if (t < 1 && this.running) requestAnimationFrame(tick);
        else resolve();
      };
      requestAnimationFrame(tick);
    });
  }

  update(dt) {
    if (!this.reduced) {
      this.flame.update(dt);
      this.oxygen.update(dt, this.oxygenLevel, this._jarBounds());
      if (this.showAirflow) this.airflow.update(dt, this.mode, this._jarBounds());
    } else {
      this.flame.strength = this.flame.targetStrength;
    }
  }

  _layout() {
    const cx = this.w * 0.5;
    const boardY = this.h * 0.78;
    const boardW = Math.min(this.w * 0.62, 420);
    const boardH = Math.max(18, this.h * 0.035);
    const scale = Math.min(this.w, this.h) / 520;
    return { cx, boardY, boardW, boardH, scale };
  }

  _jarBounds() {
    const { cx, boardY, scale } = this._layout();
    const jarW = 120 * scale * 1.15;
    const jarH = 190 * scale * 1.15;
    const jarBottom = boardY - 8;
    return {
      x: cx - jarW / 2,
      y: jarBottom - jarH,
      w: jarW,
      h: jarH,
      cx,
      bottom: jarBottom,
      top: jarBottom - jarH,
      scale,
    };
  }

  draw() {
    const { ctx, w, h } = this;
    ctx.clearRect(0, 0, w, h);

    // vignette floor light
    const floor = ctx.createRadialGradient(w * 0.5, h * 0.9, 10, w * 0.5, h * 0.85, h * 0.55);
    floor.addColorStop(0, 'rgba(255, 120, 40, 0.08)');
    floor.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = floor;
    ctx.fillRect(0, 0, w, h);

    const L = this._layout();
    const jar = this._jarBounds();

    if (this.buildStep >= 1) this._drawBoard(L);
    if (this.buildStep >= 2) this._drawClay(L);
    if (this.buildStep >= 2) {
      const flameY = L.boardY - 28 * L.scale * 1.4 - 8;
      this.flame.setPosition(L.cx, flameY, L.scale * 1.15);
      this._drawCandle(L);
      if (this.buildStep >= 3) this.flame.draw();
    }
    if (this.showOxygen && this.buildStep >= 4) {
      this.oxygen.draw(ctx, this.oxygenLevel);
    }
    if (this.buildStep >= 4) this._drawJar(jar);
    if (this.buildStep >= 5 && (this.mode === 'sealed' || this.mode === 'bottomOnly')) {
      this._drawLid(jar);
    }
    if (this.showAirflow) this.airflow.draw(ctx);
  }

  _drawBoard(L) {
    const { ctx } = this;
    const x = L.cx - L.boardW / 2;
    const y = L.boardY;
    const grad = ctx.createLinearGradient(x, y, x, y + L.boardH);
    grad.addColorStop(0, '#a67c52');
    grad.addColorStop(1, '#6e4d30');
    ctx.fillStyle = grad;
    ctx.strokeStyle = 'rgba(0,0,0,0.35)';
    ctx.lineWidth = 1;
    roundRect(ctx, x, y, L.boardW, L.boardH, 4);
    ctx.fill();
    ctx.stroke();
  }

  _drawClay(L) {
    const { ctx } = this;
    const r = 36 * L.scale;
    const cy = L.boardY - 2;
    const gaps = this.mode === 'bottomOnly' || this.mode === 'airflow';
    ctx.fillStyle = '#2f5fa8';
    ctx.beginPath();
    ctx.ellipse(L.cx, cy, r * 1.15, r * 0.42, 0, 0, Math.PI * 2);
    ctx.fill();
    if (gaps) {
      // Notch gaps so fresh air can enter (matches lesson diagrams)
      ctx.fillStyle = '#6e4d30';
      ctx.beginPath();
      ctx.ellipse(L.cx - r * 0.78, cy, 11 * L.scale, 9 * L.scale, 0, 0, Math.PI * 2);
      ctx.ellipse(L.cx + r * 0.78, cy, 11 * L.scale, 9 * L.scale, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(8, 12, 22, 0.65)';
      ctx.beginPath();
      ctx.ellipse(L.cx - r * 0.78, cy, 7 * L.scale, 5 * L.scale, 0, 0, Math.PI * 2);
      ctx.ellipse(L.cx + r * 0.78, cy, 7 * L.scale, 5 * L.scale, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  _drawCandle(L) {
    const { ctx } = this;
    const cw = 22 * L.scale;
    const ch = 48 * L.scale;
    const x = L.cx - cw / 2;
    const y = L.boardY - 10 - ch;
    const wax = ctx.createLinearGradient(x, y, x + cw, y);
    wax.addColorStop(0, '#f3ead8');
    wax.addColorStop(0.5, '#fff8ee');
    wax.addColorStop(1, '#e6d5b8');
    ctx.fillStyle = wax;
    roundRect(ctx, x, y, cw, ch, 4);
    ctx.fill();
    ctx.fillStyle = 'rgba(40, 30, 20, 0.85)';
    ctx.fillRect(L.cx - 1, y - 6, 2, 8);
  }

  _drawJar(jar) {
    const { ctx } = this;
    ctx.save();
    // glass body
    const g = ctx.createLinearGradient(jar.x, jar.y, jar.x + jar.w, jar.y);
    g.addColorStop(0, 'rgba(180, 210, 230, 0.08)');
    g.addColorStop(0.2, 'rgba(200, 230, 255, 0.22)');
    g.addColorStop(0.5, 'rgba(180, 210, 230, 0.08)');
    g.addColorStop(0.8, 'rgba(200, 230, 255, 0.18)');
    g.addColorStop(1, 'rgba(180, 210, 230, 0.1)');
    ctx.fillStyle = g;
    ctx.strokeStyle = 'rgba(190, 220, 240, 0.55)';
    ctx.lineWidth = 2;
    roundRect(ctx, jar.x, jar.y, jar.w, jar.h, 10);
    ctx.fill();
    ctx.stroke();

    // rim highlight
    ctx.strokeStyle = 'rgba(230, 250, 255, 0.35)';
    ctx.beginPath();
    ctx.moveTo(jar.x + 8, jar.y + 12);
    ctx.lineTo(jar.x + 8, jar.y + jar.h - 16);
    ctx.stroke();
    ctx.restore();
  }

  _drawLid(jar) {
    const { ctx } = this;
    const lw = jar.w * 1.08;
    const lh = 14 * jar.scale;
    const x = jar.cx - lw / 2;
    const y = jar.y - lh * 0.55;
    const metal = ctx.createLinearGradient(x, y, x, y + lh);
    metal.addColorStop(0, '#e6c65a');
    metal.addColorStop(0.5, '#c9a227');
    metal.addColorStop(1, '#8a6d18');
    ctx.fillStyle = metal;
    roundRect(ctx, x, y, lw, lh, 4);
    ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.25)';
    ctx.fillRect(x + 10, y + 3, lw * 0.35, 2);
  }
}

function roundRect(ctx, x, y, w, h, r) {
  const rr = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}
