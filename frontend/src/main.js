import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'

import axios from 'axios'

// Configure default base URL
axios.defaults.baseURL = 'http://localhost:8000/api/v1'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueApexCharts)
app.provide('axios', axios)
app.mount('#app')
