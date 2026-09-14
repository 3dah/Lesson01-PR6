# The Mystery of Fire

Premium interactive Grade 6 science experience: **The Role of Air in Burning Things**.

## Run (development)

```bash
npm install
npm run dev
```

Open `http://localhost:5173/`.

## Open directly (no server)

Chromium blocks ES modules on `file://`, so a one-time build produces a classic JS bundle:

```bash
npm run build
```

Then double-click **`index.html`** (or open it via `file://`).  
The page loads `./dist/assets/app.js` + `./dist/assets/style.css` automatically.

You can also open `dist/index.html` the same way.

## Production build

```bash
npm run build
npm run preview
```

## Learning arc

Mystery → Invisible Air → Experiment → Prediction → Closed Jar → Flame Out → Why → Fresh Air → Aha → Science → Real World → Challenge → Discovery

## Source authority

Lesson pages in `assets/source/`. Content maps in `docs/`.

## Stack

Vite · Vanilla ES modules (dev) · IIFE bundle (static/`file://`) · Canvas · GSAP · Web Audio
