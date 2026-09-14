import { App } from './app.js';

const app = new App();
app.init();

// Expose for debugging / QA
window.__mysteryOfFire = app;
