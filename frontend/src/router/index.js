import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'

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
    // Admin Routes
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/AdminDashboard.vue'),
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/cards',
        name: 'CardsManagement',
        component: () => import('../views/admin/CardsManagement.vue'),
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/flow',
        name: 'FlowEngine',
        component: () => import('../views/admin/FlowEngine.vue'),
        meta: { requiresAuth: true, role: 'admin' }
    },
    // Admin Routes
    {
        path: '/admin/login',
        name: 'AdminLogin',
        component: () => import('../views/admin/AdminLogin.vue'),
        meta: { requiresAuth: false, isAdminRoute: true }
    },
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/AdminDashboard.vue'),
        meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
    },
    {
        path: '/admin/users',
        name: 'UserManagement',
        component: () => import('../views/admin/UserManagement.vue'),
        meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
    },
    {
        path: '/admin/logs',
        name: 'AuditLogs',
        component: () => import('../views/admin/AuditLogs.vue'),
        meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
    },
    {
        path: '/admin/analytics',
        name: 'TokenAnalytics',
        component: () => import('../views/admin/TokenAnalytics.vue'),
        meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
    },
    // Portal Routes
    {
        path: '/portal/dashboard',
        name: 'PortalDashboard',
        component: () => import('../views/portal/PortalDashboard.vue'),
        meta: { requiresAuth: true }
    },
    // Legal Routes
    {
        path: '/kvkk',
        name: 'KVKK',
        component: () => import('../views/legal/KVKK.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/gizlilik-politikasi',
        name: 'PrivacyPolicy',
        component: () => import('../views/legal/PrivacyPolicy.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/teknik-gereksinimler',
        name: 'TechnicalRequirements',
        component: () => import('../views/legal/TechnicalRequirements.vue'),
        meta: { requiresAuth: false }
    },
    // Support Routes
    {
        path: '/destek',
        name: 'Support',
        component: () => import('../views/support/Support.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/iletisim',
        name: 'Contact',
        component: () => import('../views/support/Contact.vue'),
        meta: { requiresAuth: false }
    },
    // Admin Routes
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const adminStore = useAdminStore()

    // Admin routes check
    if (to.meta.requiresAdminAuth) {
        if (!adminStore.isAuthenticated) {
            // Redirect to admin login if not authenticated
            next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
            return
        }
    }

    // Regular user routes check
    if (to.meta.requiresAuth && !to.meta.requiresAdminAuth) {
        if (!authStore.isAuthenticated) {
            // Redirect to login if not authenticated
            next({ name: 'Login', query: { redirect: to.fullPath } })
            return
        }
    }

    next()
})

export default router
