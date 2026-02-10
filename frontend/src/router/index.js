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
        path: '/admin/login',
        name: 'AdminLogin',
        component: () => import('../views/admin/AdminLogin.vue'),
        meta: { requiresAuth: false, isAdminRoute: true }
    },
    {
        path: '/admin',
        component: () => import('../components/AdminLayout.vue'),
        meta: { requiresAdminAuth: true },
        children: [
            {
                path: 'dashboard',
                name: 'AdminDashboard',
                component: () => import('../views/admin/AdminDashboard.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            },
            {
                path: 'cards',
                name: 'CardsManagement',
                component: () => import('../views/admin/CardsManagement.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            },
            {
                path: 'flow',
                name: 'FlowEngine',
                component: () => import('../views/admin/FlowEngine.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            },
            {
                path: 'users',
                name: 'UserManagement',
                component: () => import('../views/admin/UserManagement.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            },
            {
                path: 'logs',
                name: 'AuditLogs',
                component: () => import('../views/admin/AuditLogs.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            },
            {
                path: 'analytics',
                name: 'TokenAnalytics',
                component: () => import('../views/admin/TokenAnalytics.vue'),
                meta: { requiresAuth: true, role: 'admin', requiresAdminAuth: true }
            }
        ]
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
    // Routes for Support and Contact are now sections in LandingPage
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

    // Admin routes check - handle these first and exclusively
    if (to.meta.requiresAdminAuth) {
        if (!adminStore.isAuthenticated) {
            // Redirect to admin login if not authenticated
            next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
            return
        }
        // Admin is authenticated, allow navigation
        next()
        return
    }

    // Regular user routes check - only for non-admin routes
    if (to.meta.requiresAuth) {
        if (!authStore.isAuthenticated) {
            // Redirect to login if not authenticated
            next({ name: 'Login', query: { redirect: to.fullPath } })
            return
        }
    }

    next()
})

// Global error handler for chunk loading errors
router.onError((error) => {
    const pattern = /Loading chunk (\d)+ failed/g;
    const isChunkLoadFailed = error.message.match(pattern);
    const targetPath = router.currentRoute.value.fullPath;

    if (isChunkLoadFailed || error.message.includes('Failed to fetch dynamically imported module')) {
        console.error('Chunk load error detected, reloading page...', error);

        // Prevent infinite reload loops
        const storageKey = 'chunk_reload_' + targetPath;
        const lastReload = sessionStorage.getItem(storageKey);
        const now = Date.now();

        if (!lastReload || now - parseInt(lastReload) > 10000) {
            sessionStorage.setItem(storageKey, now.toString());
            window.location.reload(true);
        }
    }
});

export default router
