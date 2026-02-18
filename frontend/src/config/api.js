import axios from 'axios'

// API Configuration
export const API_CONFIG = {
    // Backend base URL - use relative path for production (nginx proxy)
    BASE_URL: import.meta.env.VITE_API_BASE_URL || '/api/v1',

    // Request timeout in milliseconds
    TIMEOUT: 30000,

    // Common headers
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
}

// API Endpoints
export const API_ENDPOINTS = {
    // Health check
    HEALTH: '/health',

    // Auth endpoints
    AUTH: {
        LOGIN: '/auth/login',
        LOGOUT: '/auth/logout',
        REFRESH: '/auth/refresh',
        ME: '/auth/me',
    },

    // Add more endpoints as needed
    CUSTOMERS: '/customers',
    APPOINTMENTS: '/appointments',
    ANALYTICS: '/analytics',
}

// Create axios instance with default config
const api = axios.create({
    baseURL: API_CONFIG.BASE_URL,
    timeout: API_CONFIG.TIMEOUT,
    headers: API_CONFIG.HEADERS
})

// Request interceptor - add auth token if available
api.interceptors.request.use(
    (config) => {
        // Get token from sessionStorage
        const token = sessionStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        // Get tenant ID from sessionStorage
        const tenantId = sessionStorage.getItem('tenant_id')
        if (tenantId) {
            config.headers['X-Tenant-ID'] = tenantId
        }

        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor - handle errors globally
api.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
            // Clear auth data
            sessionStorage.removeItem('access_token')
            sessionStorage.removeItem('tenant_id')

            // Redirect to login
            if (window.location.pathname !== '/login') {
                window.location.href = '/login'
            }
        }

        return Promise.reject(error)
    }
)

export default api

