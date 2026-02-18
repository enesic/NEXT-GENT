import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { axios } from '@/plugins/axios'

export const useAdminStore = defineStore('admin', () => {
    // State
    const adminUser = ref(null)
    const accessToken = ref(sessionStorage.getItem('admin_token') || null)
    const isAuthenticated = computed(() => !!accessToken.value && !!adminUser.value)

    // Actions
    async function login(username, password) {
        try {
            const response = await axios.post('/auth/admin/login', {
                username,
                password
            })

            // API returns 'token' and 'admin', not 'access_token' and 'admin_user'
            const { token, admin } = response.data

            accessToken.value = token
            adminUser.value = admin

            // Store token in sessionStorage
            sessionStorage.setItem('admin_token', token)
            sessionStorage.setItem('admin_user', JSON.stringify(admin))

            return true
        } catch (error) {
            console.error('Login failed:', error)
            throw error
        }
    }

    async function logout() {
        try {
            // Call logout endpoint
            await axios.post('/auth/admin/logout', {}, {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })
        } catch (error) {
            console.error('Logout API call failed:', error)
        } finally {
            // Clear state regardless of API call success
            accessToken.value = null
            adminUser.value = null
            sessionStorage.removeItem('admin_token')
            sessionStorage.removeItem('admin_user')
        }
    }

    async function refreshToken() {
        try {
            const response = await axios.post('/auth/admin/refresh', {}, {
                headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }
            })

            const { access_token } = response.data
            accessToken.value = access_token
            sessionStorage.setItem('admin_token', access_token)

            return true
        } catch (error) {
            console.error('Token refresh failed:', error)
            await logout()
            return false
        }
    }

    function initializeFromStorage() {
        const storedToken = sessionStorage.getItem('admin_token')
        const storedUser = sessionStorage.getItem('admin_user')

        if (storedToken && storedUser) {
            accessToken.value = storedToken
            try {
                adminUser.value = JSON.parse(storedUser)
            } catch (e) {
                console.error('Failed to parse stored admin user:', e)
                logout()
            }
        }
    }

    // Initialize on store creation
    initializeFromStorage()

    return {
        adminUser,
        accessToken,
        isAuthenticated,
        login,
        logout,
        refreshToken
    }
})
