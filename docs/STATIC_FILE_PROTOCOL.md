# Static / file:// compatibility

## Why `file://` failed originally

1. **Absolute paths** (`/src/main.js`, `/src/styles/...`, `/favicon.svg`) resolve to the drive root under `file://`, not the project folder.
2. **Bare npm import** `import gsap from 'gsap'` cannot resolve without Vite.
3. **Chromium CORS**: ES `type="module"` scripts are blocked on `file://` (origin `null`).
4. **`crossorigin` attributes** on built CSS/JS also fail under `file://`.

## Solution (one experience)

| Mode | How it loads |
|------|----------------|
| `npm run dev` / http | ESM: `import('./src/main.js')` + `./src/styles/experience.css` |
| Double-click `index.html` | Classic scripts: `./dist/assets/app.js` (IIFE) + `./dist/assets/style.css` |
| Open `dist/index.html` | Same IIFE + CSS with relative `./assets/...` paths |

GSAP is vendored at `vendor/gsap/` for a single relative import used by the source tree (`src/app.js`).

Prerequisite for static open: run `npm run build` once so `dist/assets/` exists.
