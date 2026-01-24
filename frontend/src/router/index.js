import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Lazy-load components for better performance
const Home = () => import('../App.vue')

const routes = [
    {
        path: '/',
        name: 'LandingPage',
        component: () => import('../views/LandingPage.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/dashboard',
        name: 'ExecutiveShell',
        component: () => import('../components/ExecutiveShell.vue'),
        meta: { requiresAuth: true }
    },
    // Add more routes as needed
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Check if route requires authentication
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        // Redirect to login if not authenticated
        next({ name: 'Login', query: { redirect: to.fullPath } })
    } else {
        next()
    }
})

export default router
