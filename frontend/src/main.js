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
