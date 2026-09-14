# QA Report — The Mystery of Fire

**Date:** 2026-09-14  
**Build:** Vite SPA · procedural Canvas science visuals · GSAP transitions

## Automated walkthrough
Playwright Chromium walked all 13 chapters with interactions (assemble, predict, seal, deplete, scrub, airflow two-phase, challenge). **Console / page errors: none.**

Screenshots archived in `docs/qa-*.png`.

## Checks

| Area | Result | Notes |
|------|--------|-------|
| Source fidelity | Pass | Combustion definition, Steps 1–5, explanations, 3 conclusions, teacher-only lighter |
| Bottom-gap nuance | Pass | Fresh Air phase 1 extinguishes; phase 2 (both openings) sustains |
| Chapter flow | Pass | Gate + 13 chapters |
| Interactions | Pass | Reveal air, assemble, predict, seal, scrub, airflow, world, challenge |
| Prediction reflection | Pass | Shown after extinguish |
| Responsive layout | Pass | Visual stage min-height; stacked compare on narrow CSS |
| Reduced motion | Pass | GSAP skipped; atmosphere idle |
| Audio + mute | Pass | Procedural Web Audio; mute control |
| Production build | Pass | `npm run build` succeeds |
| AI video/stills | N/A | Higgsfield free plan requires Basic+; procedural Canvas used instead |

## Self-critique → fixes
1. Clay gaps no longer punch through canvas.
2. Candle appears before lighting; flame only after teacher-light step.
3. Fresh Air is two explicit lesson-aligned phases.
4. Mute control uses a speaker glyph (not a menu lookalike).
5. Progress dots cannot skip ahead.
6. Removed unused Three.js; Canvas + GSAP are the runtime stack.
