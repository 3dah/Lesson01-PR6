/** Lightweight procedural audio — no continuous music */
export class Soundscape {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.master = null;
    this.ambience = null;
  }

  async unlock() {
    if (this.ctx) return;
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return;
    this.ctx = new Ctx();
    this.master = this.ctx.createGain();
    this.master.gain.value = 0.35;
    this.master.connect(this.ctx.destination);
    if (this.ctx.state === 'suspended') await this.ctx.resume();
  }

  setMuted(m) {
    this.muted = m;
    if (this.master) this.master.gain.value = m ? 0 : 0.35;
    if (m) this.stopAmbience();
  }

  async startAmbience() {
    await this.unlock();
    if (!this.ctx || this.muted || this.ambience) return;
    const noise = this.ctx.createBufferSource();
    const buffer = this.ctx.createBuffer(1, this.ctx.sampleRate * 2, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * 0.4;
    noise.buffer = buffer;
    noise.loop = true;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 420;
    const gain = this.ctx.createGain();
    gain.gain.value = 0.045;
    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.master);
    noise.start();
    this.ambience = { noise, gain };
  }

  stopAmbience() {
    if (!this.ambience) return;
    try {
      this.ambience.noise.stop();
    } catch {
      /* ignore */
    }
    this.ambience = null;
  }

  async whoosh() {
    await this.unlock();
    if (!this.ctx || this.muted) return;
    const t = this.ctx.currentTime;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(180, t);
    o.frequency.exponentialRampToValueAtTime(60, t + 0.35);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.12, t + 0.04);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
    o.connect(g);
    g.connect(this.master);
    o.start(t);
    o.stop(t + 0.4);
  }

  async extinguish() {
    await this.unlock();
    if (!this.ctx || this.muted) return;
    const t = this.ctx.currentTime;
    const buffer = this.ctx.createBuffer(1, this.ctx.sampleRate * 0.4, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < data.length; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / data.length, 1.5);
    }
    const src = this.ctx.createBufferSource();
    src.buffer = buffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 900;
    const g = this.ctx.createGain();
    g.gain.value = 0.2;
    src.connect(filter);
    filter.connect(g);
    g.connect(this.master);
    src.start(t);
  }

  async click() {
    await this.unlock();
    if (!this.ctx || this.muted) return;
    const t = this.ctx.currentTime;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.frequency.value = 660;
    g.gain.setValueAtTime(0.05, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.08);
    o.connect(g);
    g.connect(this.master);
    o.start(t);
    o.stop(t + 0.09);
  }
}
