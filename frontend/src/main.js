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
console.log('🚀 NextGent System v3.0 - Loaded')
console.log('✅ Dashboard Alerts Disabled')

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueApexCharts)
app.provide('axios', axios)
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
