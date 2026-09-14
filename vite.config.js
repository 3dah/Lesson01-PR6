import { defineConfig } from 'vite';

/**
 * Dual-mode strategy:
 * - Vite/dev (http): native ESM via ./src/main.js
 * - file://: Chromium blocks ES modules (CORS/null origin), so we ship an IIFE
 *   bundle at dist/assets/app.js and load it as a classic script from root index.html
 */
export default defineConfig({
  root: '.',
  base: './',
  publicDir: 'public',
  server: {
    port: 5173,
    open: true,
  },
  build: {
    outDir: 'dist',
    assetsInlineLimit: 4096,
    cssCodeSplit: false,
    modulePreload: false,
    rollupOptions: {
      output: {
        format: 'iife',
        name: 'MysteryOfFire',
        inlineDynamicImports: true,
        entryFileNames: 'assets/app.js',
        assetFileNames: 'assets/[name][extname]',
      },
    },
  },
  plugins: [
    {
      name: 'file-protocol-html',
      apply: 'build',
      transformIndexHtml: {
        order: 'post',
        handler(html) {
          let out = html
            .replace(/<script>\s*\/\*\*[\s\S]*?file:\/\/[\s\S]*?<\/script>/gi, '')
            .replace(/<script>\s*\(function \(\) \{\s*if \(location\.protocol !== 'file:'\)[\s\S]*?<\/script>/g, '')
            .replace(/<!--[\s\S]*?-->/g, '')
            .replace(/<link[^>]*data-app-css[^>]*>/g, '')
            .replace(/<script type="module"[\s\S]*?<\/script>/g, '')
            // crossorigin on file:// triggers CORS failures for CSS/JS
            .replace(/\s+crossorigin(?:="[^"]*")?/g, '')
            .replace(/(href|src)="\/assets\//g, '$1="./assets/');

          // Deduplicate stylesheet links; keep a single relative classic CSS + JS entry
          out = out.replace(/<link\s+rel="stylesheet"[^>]*href="\.\/assets\/style\.css"[^>]*>\s*/g, '');
          out = out.replace(
            '</head>',
            '    <link rel="stylesheet" href="./assets/style.css" />\n    <script src="./assets/app.js" defer></script>\n  </head>',
          );
          // Remove any leftover module/preload scripts Vite injected
          out = out.replace(/<link\s+rel="modulepreload"[^>]*>/g, '');
          out = out.replace(/<script[^>]*type="module"[^>]*><\/script>/g, '');

          return out;
        },
      },
    },
  ],
});
