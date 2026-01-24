// API Configuration
export const API_CONFIG = {
    // Backend base URL - adjust for production
    BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',

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

export default API_CONFIG
