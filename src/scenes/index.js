import { CHAPTERS, PREDICTION_CHOICES, PREDICTION_BEST, CHALLENGE_CHOICES, CHALLENGE_BEST, CONCLUSIONS, SAFETY, REAL_WORLD } from '../data/content.js';
import { sceneShell, choiceGroup, el } from '../components/dom.js';
import { ExperimentRig } from '../animations/ExperimentRig.js';
import { FlameEngine } from '../animations/FlameEngine.js';

function canvasEl() {
  const c = el('canvas');
  c.setAttribute('aria-hidden', 'true');
  return c;
}

/** Dual rig for compare scene */
class MiniRig {
  constructor(canvas, mode) {
    this.rig = new ExperimentRig(canvas);
    this.rig.setBuildStep(5);
    this.rig.setMode(mode);
    if (mode === 'sealed') {
      this.rig.oxygenLevel = 0.15;
      this.rig.flame.setStrength(0);
    } else {
      this.rig.oxygenLevel = 1;
      this.rig.flame.setStrength(1);
      this.rig.showAirflow = true;
    }
  }
  mount() { this.rig.mount(); }
  unmount() { this.rig.unmount(); }
}

export function createScenes(app) {
  return [
    mysteryScene(app),
    airScene(app),
    experimentScene(app),
    predictionScene(app),
    closedScene(app),
    outScene(app),
    whyScene(app),
    freshScene(app),
    ahaScene(app),
    scienceScene(app),
    worldScene(app),
    challengeScene(app),
    discoveryScene(app),
  ];
}

function mysteryScene(app) {
  const ch = CHAPTERS[0];
  const canvas = canvasEl();
  let flame;
  let raf;
  let running = false;

  const { root, visualWrap, actionsWrap } = sceneShell(ch, { visual: canvas });
  const hint = el('p', 'scene-sub', { text: 'Watch the flame. Something invisible is feeding it.' });
  hint.style.marginTop = '0.5rem';
  actionsWrap.append(hint);

  return {
    id: ch.id,
    chapter: ch,
    root,
    enter() {
      root.classList.add('is-active');
      const ctx = canvas.getContext('2d');
      const resize = () => {
        const r = canvas.getBoundingClientRect();
        const dpr = Math.min(devicePixelRatio || 1, 2);
        canvas.width = r.width * dpr;
        canvas.height = r.height * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        flame?.setPosition(r.width / 2, r.height * 0.72, Math.min(r.width, r.height) / 280);
      };
      flame = new FlameEngine(ctx, { strength: 1 });
      resize();
      window.addEventListener('resize', resize);
      root._cleanup = () => window.removeEventListener('resize', resize);
      running = true;
      let last = performance.now();
      const loop = (now) => {
        if (!running) return;
        const dt = Math.min(0.05, (now - last) / 1000);
        last = now;
        const r = canvas.getBoundingClientRect();
        ctx.clearRect(0, 0, r.width, r.height);
        // soft radial stage
        const g = ctx.createRadialGradient(r.width / 2, r.height * 0.7, 10, r.width / 2, r.height * 0.75, r.height * 0.55);
        g.addColorStop(0, 'rgba(255,120,40,0.12)');
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, r.width, r.height);
        flame.update(dt);
        flame.draw();
        // candle body
        const s = flame.scale;
        ctx.fillStyle = '#f3ead8';
        const cw = 26 * s;
        const chh = 70 * s;
        roundRectPath(ctx, flame.x - cw / 2, flame.y + 2, cw, chh, 5);
        ctx.fill();
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      app.sound.startAmbience();
    },
    exit() {
      running = false;
      cancelAnimationFrame(raf);
      root._cleanup?.();
      root.classList.remove('is-active');
    },
  };
}

function airScene(app) {
  const ch = CHAPTERS[1];
  const canvas = canvasEl();
  let particles = [];
  let running = false;
  let revealed = false;
  let raf;

  const btn = el('button', 'action-btn is-air', { type: 'button', text: 'Reveal the invisible air' });
  const { root, actionsWrap } = sceneShell(ch, { visual: canvas, actions: [btn] });

  btn.addEventListener('click', () => {
    revealed = true;
    btn.disabled = true;
    btn.textContent = 'Air surrounds everything — including fire';
    app.sound.whoosh();
    app.unlockNext(true);
  });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      revealed = false;
      btn.disabled = false;
      btn.textContent = 'Reveal the invisible air';
      app.unlockNext(false);
      const ctx = canvas.getContext('2d');
      const resize = () => {
        const r = canvas.getBoundingClientRect();
        const dpr = Math.min(devicePixelRatio || 1, 2);
        canvas.width = r.width * dpr;
        canvas.height = r.height * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      };
      resize();
      particles = Array.from({ length: 70 }, () => ({
        x: Math.random(),
        y: Math.random(),
        r: 1 + Math.random() * 2.5,
        a: 0,
        ta: 0.15 + Math.random() * 0.45,
        vx: (-0.02 + Math.random() * 0.04),
        vy: (-0.03 + Math.random() * 0.01),
      }));
      running = true;
      const loop = () => {
        if (!running) return;
        const r = canvas.getBoundingClientRect();
        ctx.clearRect(0, 0, r.width, r.height);
        // candle glow center
        const gx = r.width / 2;
        const gy = r.height * 0.65;
        const glow = ctx.createRadialGradient(gx, gy, 4, gx, gy, 120);
        glow.addColorStop(0, 'rgba(255,160,60,0.35)');
        glow.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, r.width, r.height);
        ctx.fillStyle = '#f3ead8';
        roundRectPath(ctx, gx - 14, gy, 28, 70, 5);
        ctx.fill();
        // tiny flame
        ctx.fillStyle = '#ffb040';
        ctx.beginPath();
        ctx.ellipse(gx, gy - 18, 8, 22, 0, 0, Math.PI * 2);
        ctx.fill();

        for (const p of particles) {
          if (revealed) p.a += (p.ta - p.a) * 0.04;
          else p.a += (0 - p.a) * 0.08;
          p.x += p.vx * 0.016;
          p.y += p.vy * 0.016;
          if (p.x < 0) p.x = 1;
          if (p.x > 1) p.x = 0;
          if (p.y < 0) p.y = 1;
          ctx.fillStyle = `rgba(122, 215, 255, ${p.a})`;
          ctx.beginPath();
          ctx.arc(p.x * r.width, p.y * r.height, p.r, 0, Math.PI * 2);
          ctx.fill();
        }
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      root._onResize = resize;
      window.addEventListener('resize', resize);
    },
    exit() {
      running = false;
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', root._onResize);
      root.classList.remove('is-active');
    },
  };
}

function experimentScene(app) {
  const ch = CHAPTERS[2];
  const canvas = canvasEl();
  const caution = el('p', 'caution', { text: SAFETY });
  const btn = el('button', 'action-btn is-primary', { type: 'button', text: 'Assemble the next piece' });
  const label = el('p', 'feedback', { text: '' });
  const { root, actionsWrap } = sceneShell(ch, { visual: canvas, actions: [caution, btn, label] });
  let rig;
  let step = 0;
  const steps = [
    'Wooden board in place.',
    'Clay spread — candle fixed on the clay.',
    'Teacher lights the candle. (Students do not use the lighter.)',
    'Bottomless jar covers the candle — top left open.',
    'Apparatus ready. Next: predict, then seal.',
  ];

  btn.addEventListener('click', () => {
    step = Math.min(5, step + 1);
    rig.setBuildStep(step);
    if (step < 3) {
      rig.flame.setStrength(0, true);
    }
    if (step === 3) {
      rig.setMode('free');
      rig.flame.setStrength(1);
    }
    if (step === 4) {
      rig.setMode('openTop');
      rig.flame.setStrength(1);
    }
    label.textContent = steps[step - 1] || '';
    app.sound.click();
    if (step >= 5) {
      btn.disabled = true;
      btn.textContent = 'Setup complete';
      app.unlockNext(true);
    }
  });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      step = 0;
      btn.disabled = false;
      btn.textContent = 'Assemble the next piece';
      label.textContent = 'Tap to build: board → clay & candle → light → jar';
      app.unlockNext(false);
      rig = new ExperimentRig(canvas);
      rig.setBuildStep(0);
      rig.setMode('free');
      rig.flame.setStrength(0);
      rig.mount();
    },
    exit() {
      rig?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function predictionScene(app) {
  const ch = CHAPTERS[3];
  const visual = el('div');
  visual.style.cssText = 'display:grid;place-items:center;height:100%;padding:1rem;color:#9aa6b8;font-size:0.95rem;text-align:center;';
  visual.textContent = 'Make your prediction before we seal the jar.';
  const feedback = el('p', 'feedback');
  const choices = choiceGroup(PREDICTION_CHOICES, {
    name: 'Prediction',
    onSelect: (id) => {
      app.state.prediction = id;
      app.sound.click();
      feedback.textContent =
        id === PREDICTION_BEST
          ? 'Interesting — let’s test it. (No spoilers yet.)'
          : 'Noted. Let’s run the experiment and see.';
      app.unlockNext(true);
    },
  });
  const { root, actionsWrap } = sceneShell(ch, { visual, actions: [choices, feedback] });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      app.unlockNext(!!app.state.prediction);
      feedback.textContent = app.state.prediction ? 'Prediction saved. Continue when ready.' : '';
    },
    exit() {
      root.classList.remove('is-active');
    },
  };
}

function closedScene(app) {
  const ch = CHAPTERS[4];
  const canvas = canvasEl();
  const btn = el('button', 'action-btn is-primary', { type: 'button', text: 'Place the metal lid' });
  const meterWrap = el('div');
  meterWrap.style.cssText = 'display:grid;gap:0.35rem;justify-items:center;width:100%;';
  const meterLabel = el('p', 'scene-sub', { text: 'Available air inside the jar' });
  const meter = el('div', 'meter');
  const fill = el('span');
  meter.append(fill);
  meterWrap.append(meterLabel, meter);
  const { root, actionsWrap } = sceneShell(ch, { visual: canvas, actions: [btn, meterWrap] });
  let rig;
  let sealed = false;

  btn.addEventListener('click', async () => {
    if (sealed) return;
    sealed = true;
    btn.disabled = true;
    btn.textContent = 'Jar sealed — air is trapped';
    rig.setBuildStep(5);
    rig.setMode('sealed');
    rig.showOxygen = true;
    app.sound.whoosh();
    const start = performance.now();
    await new Promise((resolve) => {
      const tick = (now) => {
        const t = Math.min(1, (now - start) / 4500);
        const level = 1 - t * 0.55;
        rig.setOxygenLevel(level);
        fill.style.transform = `scaleX(${level})`;
        if (t < 1) requestAnimationFrame(tick);
        else resolve();
      };
      requestAnimationFrame(tick);
    });
    app.unlockNext(true);
  });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      sealed = false;
      btn.disabled = false;
      btn.textContent = 'Place the metal lid';
      fill.style.transform = 'scaleX(1)';
      app.unlockNext(false);
      rig = new ExperimentRig(canvas);
      rig.setBuildStep(5);
      rig.setMode('openTop');
      // Temporarily show without lid until sealed — buildStep 5 draws lid for sealed modes only
      rig.setMode('openTop');
      rig.setBuildStep(4);
      rig.showOxygen = true;
      rig.setOxygenLevel(1);
      rig.mount();
    },
    exit() {
      rig?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function outScene(app) {
  const ch = CHAPTERS[5];
  const canvas = canvasEl();
  const status = el('p', 'feedback', { text: 'Watch closely…' });
  const { root, actionsWrap } = sceneShell(ch, { visual: canvas, actions: [status] });
  let rig;

  return {
    id: ch.id,
    chapter: ch,
    root,
    enter() {
      root.classList.add('is-active');
      status.textContent = 'The flame gradually weakens…';
      app.unlockNext(false);
      rig = new ExperimentRig(canvas);
      rig.setBuildStep(5);
      rig.setMode('sealed');
      rig.showOxygen = true;
      rig.setOxygenLevel(0.55);
      rig.mount();
      (async () => {
        await rig.deplete(5.2);
        status.textContent = 'THE FLAME GOES OUT.';
        status.style.color = '#ffb0a8';
        status.style.fontFamily = 'Fraunces, serif';
        status.style.fontSize = '1.35rem';
        app.sound.extinguish();
        if (app.state.prediction) {
          const pick = PREDICTION_CHOICES.find((c) => c.id === app.state.prediction);
          const reflection = el('p', 'feedback');
          reflection.style.marginTop = '0.5rem';
          if (app.state.prediction === PREDICTION_BEST) {
            reflection.textContent = `Your prediction was strong: “${pick.text}” — that matches what we observed.`;
            reflection.style.color = '#9efff0';
          } else {
            reflection.textContent = `You predicted: “${pick?.text}”. Observation: the flame gradually weakened, then went out.`;
            reflection.style.color = '#ffc2bc';
          }
          actionsWrap.append(reflection);
        }
        app.unlockNext(true);
      })();
    },
    exit() {
      rig?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function whyScene(app) {
  const ch = CHAPTERS[6];
  const canvas = canvasEl();
  const scrub = el('input', '', {
    type: 'range',
    min: '0',
    max: '100',
    value: '100',
    'aria-label': 'Air remaining inside the closed jar',
  });
  scrub.style.width = 'min(100%, 280px)';
  const read = el('p', 'feedback', { text: 'Drag to use up the air inside the closed jar.' });
  const { root, actionsWrap } = sceneShell(ch, {
    visual: canvas,
    actions: [scrub, read],
  });
  let rig;

  scrub.addEventListener('input', () => {
    const level = Number(scrub.value) / 100;
    rig.setOxygenLevel(level);
    if (level < 0.08) {
      read.textContent = 'Air used up → the candle goes out.';
      app.unlockNext(true);
    } else {
      read.textContent = `Air remaining: ${Math.round(level * 100)}%`;
    }
  });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      scrub.value = '100';
      read.textContent = 'Drag to use up the air inside the closed jar.';
      app.unlockNext(false);
      rig = new ExperimentRig(canvas);
      rig.setBuildStep(5);
      rig.setMode('sealed');
      rig.showOxygen = true;
      rig.setOxygenLevel(1);
      rig.mount();
    },
    exit() {
      rig?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function freshScene(app) {
  const ch = CHAPTERS[7];
  const canvas = canvasEl();
  const btn = el('button', 'action-btn is-air', { type: 'button', text: '1 · Test bottom gap only (lid stays on)' });
  const note = el('p', 'feedback', {
    text: 'From the lesson: a bottom gap alone still lets the flame go out — only a bit later.',
  });
  const { root, actionsWrap } = sceneShell(ch, { visual: canvas, actions: [btn, note] });
  let rig;
  let phase = 0;

  btn.addEventListener('click', async () => {
    app.sound.whoosh();
    if (phase === 0) {
      phase = 1;
      btn.disabled = true;
      rig.setMode('bottomOnly');
      rig.setOxygenLevel(0.85);
      note.textContent = 'Bottom gap only… air cannot fully renew. The flame still weakens.';
      await rig.deplete(3.8);
      note.textContent = 'It goes out after a slightly longer time — matching the lesson observation.';
      btn.disabled = false;
      btn.textContent = '2 · Remove the lid (top + bottom open)';
    } else {
      phase = 2;
      rig.setMode('airflow');
      rig.setOxygenLevel(1);
      rig.flame.setStrength(1);
      btn.disabled = true;
      btn.textContent = 'Air is constantly renewed';
      note.textContent = 'Fresh air enters below. Warm air leaves above. The candle continues burning.';
      note.style.color = '#9efff0';
      app.unlockNext(true);
    }
  });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      phase = 0;
      btn.disabled = false;
      btn.textContent = '1 · Test bottom gap only (lid stays on)';
      note.style.color = '';
      note.textContent =
        'From the lesson: a bottom gap alone still lets the flame go out — only a bit later.';
      app.unlockNext(false);
      rig = new ExperimentRig(canvas);
      rig.setBuildStep(5);
      rig.setMode('sealed');
      rig.showOxygen = true;
      rig.setOxygenLevel(1);
      rig.flame.setStrength(1);
      rig.mount();
    },
    exit() {
      rig?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function ahaScene(app) {
  const ch = CHAPTERS[8];
  const compare = el('div', 'compare');
  const left = el('div', 'compare-panel');
  const right = el('div', 'compare-panel');
  left.append(el('p', 'compare-label closed', { text: 'Closed' }));
  right.append(el('p', 'compare-label airflow', { text: 'Airflow' }));
  const c1 = canvasEl();
  const c2 = canvasEl();
  c1.style.height = '100%';
  c2.style.height = '100%';
  left.append(c1);
  right.append(c2);
  compare.append(left, right);
  const note = el('p', 'feedback', {
    text: 'Closed: air is used up → flame out. Openings top & bottom: air renewed → flame continues.',
  });
  const { root, actionsWrap } = sceneShell(ch, { visual: compare, actions: [note] });
  let a;
  let b;

  return {
    id: ch.id,
    chapter: ch,
    root,
    enter() {
      root.classList.add('is-active');
      a = new MiniRig(c1, 'sealed');
      b = new MiniRig(c2, 'airflow');
      a.mount();
      b.mount();
    },
    exit() {
      a?.unmount();
      b?.unmount();
      root.classList.remove('is-active');
    },
  };
}

function scienceScene(app) {
  const ch = CHAPTERS[9];
  const visual = el('div');
  visual.style.cssText = 'display:grid;place-items:center;height:100%;padding:1.25rem;gap:1.25rem;';
  const eq = el('div', 'equation', { role: 'img', 'aria-label': 'Fuel plus oxygen plus heat yields combustion which produces heat and light' });
  eq.append(
    el('span', 'eq-chip fuel', { text: 'Fuel' }),
    el('span', 'eq-op', { text: '+' }),
    el('span', 'eq-chip oxygen', { text: 'Oxygen' }),
    el('span', 'eq-op', { text: '+' }),
    el('span', 'eq-chip heat', { text: 'Heat' }),
    el('span', 'eq-op', { text: '→' }),
    el('span', 'eq-chip result', { text: 'Heat + Light' }),
  );
  const def = el('p', 'scene-sub');
  def.style.maxWidth = '34rem';
  def.textContent =
    'Burning (combustion) is a reaction (combination) that occurs between oxygen and a substance that produces heat and light.';
  visual.append(eq, def);
  const { root } = sceneShell(ch, { visual });

  return {
    id: ch.id,
    chapter: ch,
    root,
    enter() {
      root.classList.add('is-active');
      app.sound.click();
    },
    exit() {
      root.classList.remove('is-active');
    },
  };
}

function worldScene(app) {
  const ch = CHAPTERS[10];
  const grid = el('div', 'world-grid');
  const detail = el('p', 'feedback', { text: 'Select an example to connect it to our experiment.' });
  REAL_WORLD.forEach((item) => {
    const card = el('button', 'world-card', { type: 'button' });
    card.append(el('h3', '', { text: item.title }), el('p', '', { text: item.text }));
    card.addEventListener('click', () => {
      grid.querySelectorAll('.world-card').forEach((c) => c.classList.remove('is-active'));
      card.classList.add('is-active');
      detail.textContent = item.text;
      app.sound.click();
      app.state.worldExplored = (app.state.worldExplored || 0) + 1;
      if (app.state.worldExplored >= 1) app.unlockNext(true);
    });
    grid.append(card);
  });
  const { root, actionsWrap } = sceneShell(ch, { visual: grid, actions: [detail] });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      app.state.worldExplored = 0;
      app.unlockNext(false);
      detail.textContent = 'Select an example to connect it to our experiment.';
    },
    exit() {
      root.classList.remove('is-active');
    },
  };
}

function challengeScene(app) {
  const ch = CHAPTERS[11];
  const visual = el('div');
  visual.style.cssText = 'display:grid;place-items:center;height:100%;padding:1rem;text-align:center;color:#9aa6b8;';
  visual.innerHTML =
    '<p style="max-width:28rem;line-height:1.5">Candle A is fully sealed. Candle B has only a bottom gap (lid on). Candle C has a bottom gap and an open top.</p>';
  const feedback = el('p', 'feedback');
  const choices = choiceGroup(CHALLENGE_CHOICES, {
    name: 'Challenge',
    onSelect: (id, btn, buttons) => {
      app.state.challenge = id;
      app.sound.click();
      buttons.forEach((b) => {
        b.classList.remove('is-correct', 'is-wrong');
        b.disabled = true;
      });
      if (id === CHALLENGE_BEST) {
        btn.classList.add('is-correct');
        feedback.textContent =
          'Yes! With openings at the bottom and top, air is constantly renewed — so burning can continue.';
        feedback.style.color = '#9efff0';
      } else {
        btn.classList.add('is-wrong');
        const correct = buttons.find((b) => b.dataset.id === CHALLENGE_BEST);
        correct?.classList.add('is-correct');
        feedback.textContent =
          id === 'bottom'
            ? 'Close — but a bottom gap alone still lets the flame go out after a slightly longer time. Both openings are needed.'
            : 'A sealed jar uses up its air and the flame goes out. Candle C keeps airflow going.';
        feedback.style.color = '#ffc2bc';
      }
      app.unlockNext(true);
    },
  });
  const { root, actionsWrap } = sceneShell(ch, { visual, actions: [choices, feedback] });

  return {
    id: ch.id,
    chapter: ch,
    root,
    requiresAction: true,
    enter() {
      root.classList.add('is-active');
      feedback.textContent = '';
      app.unlockNext(!!app.state.challenge);
    },
    exit() {
      root.classList.remove('is-active');
    },
  };
}

function discoveryScene(app) {
  const ch = CHAPTERS[12];
  const visual = el('div');
  visual.style.cssText = 'display:grid;place-items:center;height:100%;padding:1rem;';
  const list = el('ol', 'discovery-list');
  CONCLUSIONS.forEach((c) => {
    const li = el('li');
    li.innerHTML = c.replace('fresh air', '<strong>fresh air</strong>');
    list.append(li);
  });
  visual.append(list);
  const end = el('p', 'feedback', {
    text: 'Investigation complete. Air is invisible — but essential for a flame to keep burning.',
  });
  end.style.color = '#9efff0';
  const { root, actionsWrap } = sceneShell(ch, { visual, actions: [end] });

  return {
    id: ch.id,
    chapter: ch,
    root,
    enter() {
      root.classList.add('is-active');
      app.unlockNext(false);
      const next = document.getElementById('next-btn');
      next.textContent = 'Replay';
      next.disabled = false;
    },
    exit() {
      root.classList.remove('is-active');
      document.getElementById('next-btn').textContent = 'Continue';
    },
  };
}

function roundRectPath(ctx, x, y, w, h, r) {
  const rr = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}
