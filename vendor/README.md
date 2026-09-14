# Vendored dependencies (static / file:// support)

These ESM files are copied from npm packages so the experience can load via `file://` without Vite resolving bare package names.

| Package | Path | Version |
|---------|------|---------|
| GSAP | `vendor/gsap/` (`index.js`, `gsap-core.js`, `CSSPlugin.js`) | 3.15.0 |

Source of truth for app code remains `src/`. Vite continues to work with the same relative import: `../vendor/gsap/index.js`.
