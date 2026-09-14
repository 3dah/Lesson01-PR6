# Technical Architecture

## Stack
- **Vite** — bundling
- **Vanilla ES modules** — scene architecture
- **Canvas 2D** — flame, apparatus, oxygen, airflow (scientifically controllable)
- **GSAP** — chapter transitions
- **Web Audio API** — procedural ambience & cues

## Why Canvas over AI video
Interactive sealed vs airflow states must stay under learner control. Procedural visuals match Steps 3–5 observations precisely. Higgsfield generation required a paid plan and was unavailable.

## Module Map
```
index.html
src/
  main.js
  app.js                 — router, progress, mute, keyboard
  data/content.js        — source-aligned copy
  styles/experience.css
  components/
    Atmosphere.js
    dom.js
  scenes/
    index.js             — all 13 chapter factories
  particles/
    OxygenField.js
    AirflowSystem.js
  animations/
    FlameEngine.js
    ExperimentRig.js
  audio/
    Soundscape.js
  utils/
    math.js
assets/source/           — authoritative lesson scans
docs/                    — content & architecture docs
```

## Performance
- Particle budget scales with CPU cores and viewport width
- Each chapter unmounts its Canvas RAF loop on exit
- GSAP skipped when `prefers-reduced-motion`
- DPR capped at 2

## Accessibility
- Banner / main / contentinfo landmarks
- Keyboard: Enter on gate, ArrowLeft/Right for navigation when unlocked
- Focus-visible rings on controls
- Mute always available
- Choice groups use `role="radiogroup"`
