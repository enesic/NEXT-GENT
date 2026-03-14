import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

/**
 * Authentication Store
 * Manages user authentication state and tenant information
 */
export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref(JSON.parse(sessionStorage.getItem('user')) || null)
    const tenant_id = ref(sessionStorage.getItem('tenant_id') || null)
    const token = ref(sessionStorage.getItem('auth_token') || null)

    // Initialize Axios Header
    if (token.value) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }

    // Getters
    const isAuthenticated = computed(() => !!token.value && !!user.value)
    const hasTenant = computed(() => !!tenant_id.value)

    // Actions
    const setUser = (userData) => {
        user.value = userData
        if (userData) {
            sessionStorage.setItem('user', JSON.stringify(userData))
        } else {
            sessionStorage.removeItem('user')
        }
    }

    const setToken = (authToken) => {
        token.value = authToken
        if (authToken) {
            sessionStorage.setItem('auth_token', authToken)
            axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`
        } else {
            sessionStorage.removeItem('auth_token')
            delete axios.defaults.headers.common['Authorization']
        }
    }

    const setTenant = (tenantId) => {
        tenant_id.value = tenantId
        if (tenantId) {
            sessionStorage.setItem('tenant_id', tenantId)
            axios.defaults.headers.common['X-Tenant-ID'] = tenantId
        } else {
            sessionStorage.removeItem('tenant_id')
            delete axios.defaults.headers.common['X-Tenant-ID']
        }
    }

    // Initial Tenant Header
    if (tenant_id.value) {
        axios.defaults.headers.common['X-Tenant-ID'] = tenant_id.value
    }

    const login = async (credentials) => {
        // This logic is primarily handled in Login.vue now
        // but kept here for potential future use or testing
        return true
    }

    const logout = () => {
        user.value = null
        token.value = null
        sessionStorage.removeItem('auth_token')
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('current_sector')
        delete axios.defaults.headers.common['Authorization']

        // Optional: Clear tenant on logout? Usually kept for convenience.
        // setTenant(null) 
    }

    const clearAll = () => {
        setUser(null)
        setToken(null)
        setTenant(null)
    }

    return {
        // State
        user,
        tenant_id,
        token,

        // Getters
        isAuthenticated,
        hasTenant,

        // Actions
        setUser,
        setToken,
        setTenant,
        login,
        logout,
        clearAll,
    }
})
