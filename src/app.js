import { CHAPTERS } from './data/content.js';
import { createScenes } from './scenes/index.js';
import { Soundscape } from './audio/Soundscape.js';
import { Atmosphere } from './components/Atmosphere.js';
import { el } from './components/dom.js';
import gsap from '../vendor/gsap/index.js';
import { prefersReducedMotion } from './utils/math.js';

export class App {
  constructor() {
    this.state = {
      prediction: null,
      challenge: null,
      worldExplored: 0,
    };
    this.index = 0;
    this.sound = new Soundscape();
    this.scenes = createScenes(this);
    this.stage = document.getElementById('stage');
    this.backBtn = document.getElementById('back-btn');
    this.nextBtn = document.getElementById('next-btn');
    this.chapterLabel = document.getElementById('chapter-label');
    this.progress = document.getElementById('progress');
    this.muteBtn = document.getElementById('mute-btn');
    this.gate = document.getElementById('gate');
    this.enterBtn = document.getElementById('enter-btn');
    this._nextLocked = false;
    this.reduced = prefersReducedMotion();
  }

  init() {
    this._buildProgress();
    this.atmosphere = new Atmosphere(document.getElementById('atmosphere'));
    this.atmosphere.mount();

    this.enterBtn.addEventListener('click', async () => {
      await this.sound.unlock();
      await this.sound.startAmbience();
      this.gate.classList.add('is-hidden');
      this.show(0);
    });

    this.backBtn.addEventListener('click', () => this.prev());
    this.nextBtn.addEventListener('click', () => {
      if (this.index >= this.scenes.length - 1) {
        this.show(0);
        return;
      }
      this.next();
    });

    this.muteBtn.addEventListener('click', () => {
      const muted = this.muteBtn.getAttribute('aria-pressed') === 'true';
      const next = !muted;
      this.muteBtn.setAttribute('aria-pressed', String(next));
      this.muteBtn.setAttribute('aria-label', next ? 'Unmute sound' : 'Mute sound');
      this.sound.setMuted(next);
      if (!next) this.sound.startAmbience();
    });

    window.addEventListener('keydown', (e) => {
      if (this.gate && !this.gate.classList.contains('is-hidden')) {
        if (e.key === 'Enter') this.enterBtn.click();
        return;
      }
      if (e.key === 'ArrowRight' && !this.nextBtn.disabled) this.nextBtn.click();
      if (e.key === 'ArrowLeft' && !this.backBtn.disabled) this.backBtn.click();
    });
  }

  _buildProgress() {
    this.progress.innerHTML = '';
    CHAPTERS.forEach((ch, i) => {
      const dot = el('button', 'progress-dot', {
        type: 'button',
        title: ch.label,
        'aria-label': `Go to ${ch.label}`,
      });
      dot.addEventListener('click', () => {
        if (i <= this.index) this.show(i);
      });
      this.progress.append(dot);
    });
  }

  unlockNext(unlocked) {
    this._nextLocked = !unlocked;
    if (this.index >= this.scenes.length - 1) {
      this.nextBtn.disabled = false;
      return;
    }
    this.nextBtn.disabled = !unlocked;
  }

  show(i) {
    const prev = this.scenes[this.index];
    if (prev && prev.root.parentElement) {
      prev.exit?.();
      prev.root.remove();
    }

    this.index = i;
    const scene = this.scenes[i];
    this.stage.append(scene.root);

    if (this.reduced) {
      scene.root.classList.add('is-active');
    } else {
      gsap.fromTo(
        scene.root,
        { autoAlpha: 0, y: 18 },
        {
          autoAlpha: 1,
          y: 0,
          duration: 0.7,
          ease: 'power3.out',
          onStart: () => scene.root.classList.add('is-active'),
        },
      );
    }

    scene.enter?.();

    this.backBtn.disabled = i === 0;
    this.chapterLabel.textContent = `${String(i + 1).padStart(2, '0')} / ${String(CHAPTERS.length).padStart(2, '0')} · ${scene.chapter.label}`;

    [...this.progress.children].forEach((dot, di) => {
      dot.setAttribute('aria-current', di === i ? 'true' : 'false');
      dot.classList.toggle('is-done', di < i);
    });

    if (scene.requiresAction) this.unlockNext(false);
    else this.unlockNext(true);

    if (i < this.scenes.length - 1) this.nextBtn.textContent = 'Continue';
  }

  next() {
    if (this.index < this.scenes.length - 1) this.show(this.index + 1);
  }

  prev() {
    if (this.index > 0) this.show(this.index - 1);
  }
}
