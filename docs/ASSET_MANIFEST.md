# Asset Manifest

| Filename | Type | Purpose | Source | Generation | License |
|----------|------|---------|--------|------------|---------|
| `assets/source/lesson-page-1.jpeg` | image | Authoritative lesson: intro, combustion definition, materials | Teacher-provided PRP6 | Original scan/photo | Project source material |
| `assets/source/lesson-page-2.jpeg` | image | Authoritative explanation + conclusions | Teacher-provided PRP6 | Original | Project source material |
| `assets/source/lesson-page-3.jpeg` | image | Authoritative steps & observations | Teacher-provided PRP6 | Original | Project source material |
| Procedural flame (Canvas) | runtime | Hero flame, weaken, extinguish | `src/animations/FlameEngine.js` | Runtime procedural | Original code |
| Procedural experiment rig | runtime | Candle, clay, board, jar, lid | `src/animations/ExperimentRig.js` | Runtime Canvas | Original code |
| Oxygen / airflow particles | runtime | Invisible air made visible | `src/particles/*` | Runtime Canvas | Original code |
| Real-world vignettes | runtime | Campfire, stove, fireplace, engine metaphors | CSS + Canvas icon scenes | Runtime illustration | Original code |
| Ambient audio | runtime | Soft fire / whoosh / extinguish | Web Audio API synthesis | Procedural | Original code |
| `vendor/gsap/*` | JS ESM | Animation transitions | Copied from gsap@3.15.0 | Vendored for file:// | GSAP standard license |
| `dist/assets/app.js` | IIFE bundle | Static/`file://` entry (classic script) | `npm run build` | Vite IIFE build | Project build output |
| `dist/assets/style.css` | CSS | Static/`file://` styles | `npm run build` | Vite extract | Project build output |

**Note:** Higgsfield image/video generation was unavailable on the free plan (requires Basic+). All visuals are original procedural/runtime assets — preferable for scientifically controllable experiment states.

**Static open:** Chromium blocks ES modules on `file://`. Root `index.html` detects `file:` and loads the IIFE from `dist/assets/`. See `docs/STATIC_FILE_PROTOCOL.md`.
