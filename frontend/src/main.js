// Version: 1.0.1 - Force Rebuild
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'

import axios from 'axios'

// Configure default base URL
// Use relative URL for production (nginx proxy) or localhost for development
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
if (import.meta.env.DEV) {
    console.log('🚀 NextGent System v3.0 - Loaded')
}

// ── Settings Bootstrap ──────────────────────────────────────────────────────
// Apply saved user settings BEFORE Vue mounts so body classes are set
// immediately on every page load/refresh (not just when SettingsView is open).
; (function applyBootstrapSettings() {
    try {
        const raw = localStorage.getItem('user_settings')
        if (!raw) return
        const saved = JSON.parse(raw)
        const appearance = saved?.appearance || {}

        // Dark / light mode
        if (appearance.darkMode === false) {
            document.body.classList.add('light-mode')
        } else {
            document.body.classList.remove('light-mode')
        }

        // High contrast
        document.body.classList.toggle('high-contrast', !!appearance.highContrast)

        // Compact view
        document.body.classList.toggle('compact-view', !!appearance.compactView)
    } catch (e) {
        // Silently ignore corrupt data
    }
})()
// ────────────────────────────────────────────────────────────────────────────

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueApexCharts)
app.provide('axios', axios)
app.config.errorHandler = (err, instance, info) => {
    console.error('Global Vue Error:', err)
    console.error('Component:', instance)
    console.error('Info:', info)

    // Show error on screen (Critical for debugging Black Screen)
    const errorBox = document.createElement('div')
    errorBox.style.position = 'fixed'
    errorBox.style.top = '0'
    errorBox.style.left = '0'
    errorBox.style.width = '100%'
    errorBox.style.height = '100%'
    errorBox.style.backgroundColor = '#000'
    errorBox.style.color = '#ff4444'
    errorBox.style.zIndex = '99999'
    errorBox.style.padding = '20px'
    errorBox.style.fontFamily = 'monospace'
    errorBox.style.overflow = 'auto'
    errorBox.innerHTML = `
        <h1>Application Crash</h1>
        <p>A critical error occurred preventing the app from loading.</p>
        <pre style="background: #111; padding: 10px; border: 1px solid #333; white-space: pre-wrap;">${err.stack || err.message}</pre>
        <p>Info: ${info}</p>
        <button onclick="location.reload()" style="padding: 10px 20px; background: #333; color: white; border: none; cursor: pointer; margin-top: 20px;">Reload App</button>
    `
    document.body.appendChild(errorBox)
}

app.mount('#app')

// Global error handler for dynamic import failures (Proactive Reload)
window.addEventListener('unhandledrejection', (event) => {
    // Check for common chunk load errors
    const isChunkLoadFailed = event.reason && (
        (event.reason.message && event.reason.message.includes('Failed to fetch dynamically imported module')) ||
        (event.reason.message && event.reason.message.includes('Importing a module script failed')) ||
        (event.reason.name === 'ChunkLoadError')
    );

    if (isChunkLoadFailed) {
        console.error('Dynamic import failed (likely stale cache). Reloading page...', event.reason);

        const storageKey = 'global_chunk_reload_' + window.location.pathname;
        const lastReload = sessionStorage.getItem(storageKey);
        const now = Date.now();

        // Limit reloads to once every 5 seconds to prevent frenzied loops, 
        // but allow quick recovery if it happens again on a different route
        if (!lastReload || now - parseInt(lastReload) > 5000) {
            sessionStorage.setItem(storageKey, now.toString());
            window.location.reload(true);
        }
    }
});
