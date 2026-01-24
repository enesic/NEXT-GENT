import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * Authentication Store
 * Manages user authentication state and tenant information
 */
export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref(null)
    const tenant_id = ref(localStorage.getItem('tenant_id') || null)
    const token = ref(localStorage.getItem('auth_token') || null)

    // Getters
    const isAuthenticated = computed(() => !!token.value && !!user.value)
    const hasTenant = computed(() => !!tenant_id.value)

    // Actions
    const setUser = (userData) => {
        user.value = userData
    }

    const setToken = (authToken) => {
        token.value = authToken
        if (authToken) {
            localStorage.setItem('auth_token', authToken)
        } else {
            localStorage.removeItem('auth_token')
        }
    }

    const setTenant = (tenantId) => {
        tenant_id.value = tenantId
        if (tenantId) {
            localStorage.setItem('tenant_id', tenantId)
        } else {
            localStorage.removeItem('tenant_id')
        }
    }

    const login = async (credentials) => {
        // This will be implemented with actual API call
        // For now, just a placeholder
        try {
            // const response = await api.post('/auth/login', credentials)
            // setToken(response.data.token)
            // setUser(response.data.user)
            // setTenant(response.data.tenant_id)

            // Temporary mock for development
            setToken('mock-token-' + Date.now())
            setUser({ id: 1, name: 'Demo User', email: 'demo@nextgent.com' })
            setTenant(credentials.tenant_id || 'default-tenant')

            return true
        } catch (error) {
            console.error('Login failed:', error)
            return false
        }
    }

    const logout = () => {
        user.value = null
        token.value = null
        // Note: We keep tenant_id for convenience
        localStorage.removeItem('auth_token')
    }

    const clearAll = () => {
        user.value = null
        token.value = null
        tenant_id.value = null
        localStorage.removeItem('auth_token')
        localStorage.removeItem('tenant_id')
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
