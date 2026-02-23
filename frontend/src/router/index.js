import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'
import { useSectorStore } from '../stores/sector'
import { sectorThemes } from '../config/sectorThemes'

const validSectorIds = Object.keys(sectorThemes || {})

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
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'PortalDashboard',
                component: () => import('../views/portal/PortalDashboard.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'portal',
                name: 'PortalDashboardAlt',
                redirect: { name: 'PortalDashboard' }
            },
            {
                path: 'sectors/:sectorId',
                name: 'SectorDashboard',
                component: () => import('../views/portal/PortalDashboard.vue'),
                meta: { requiresAuth: true },
                beforeEnter(to, from, next) {
                    const id = to.params.sectorId
                    if (validSectorIds.includes(id)) {
                        const sectorStore = useSectorStore()
                        sectorStore.setSector(id)
                        next()
                    } else {
                        next({ name: 'PortalDashboard' })
                    }
                }
            },
            {
                path: 'appointments',
                name: 'Appointments',
                component: () => import('../views/CalendarView.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'messages',
                name: 'PortalMessages',
                component: () => import('../views/portal/PortalMessages.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'calls',
                name: 'PortalCalls',
                component: () => import('../views/portal/PortalCalls.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'satisfaction',
                name: 'PortalSatisfaction',
                component: () => import('../views/portal/PortalSatisfaction.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'documents',
                name: 'Documents',
                component: () => import('../views/DocumentsView.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'calendar',
                name: 'Calendar',
                component: () => import('../views/CalendarView.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'settings',
                name: 'Settings',
                component: () => import('../views/SettingsView.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'admin-dashboard',
                name: 'ShellAdminDashboard',
                component: () => import('../views/admin/AdminDashboard.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'users',
                name: 'ShellUserManagement',
                component: () => import('../views/admin/UserManagement.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'cards',
                name: 'ShellCardsManagement',
                component: () => import('../views/admin/CardsManagement.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'flows',
                name: 'ShellFlowEngine',
                component: () => import('../views/admin/FlowEngine.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'audits',
                name: 'ShellAuditLogs',
                component: () => import('../views/admin/AuditLogs.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: 'analytics',
                name: 'ShellAnalytics',
                component: () => import('../views/AnalyticsView.vue'),
                meta: { requiresAuth: true }
            }
        ]
    },
    // Legacy URL redirects
    {
        path: '/portal/dashboard',
        redirect: '/dashboard/portal'
    },
    {
        path: '/sectors/:sector/dashboard',
        redirect: to => ({ path: `/dashboard/sectors/${to.params.sector}` })
    },
    {
        path: '/sectors/:sector',
        redirect: to => ({ path: `/dashboard/sectors/${to.params.sector}` })
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
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
    // Legacy /sectors/... → nested /dashboard/sectors/...
    if (to.path.startsWith('/sectors/')) {
        const segment = to.path.replace(/^\/sectors\//, '').split('/')[0]
        next('/dashboard/sectors/' + segment)
        return
    }

    const authStore = useAuthStore()
    const adminStore = useAdminStore()

    // Admin routes check - handle these first and exclusively
    if (to.meta.requiresAdminAuth) {
        if (!adminStore.isAuthenticated) {
            next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
            return
        }
        next()
        return
    }

    // Regular user routes check - only for non-admin routes
    if (to.meta.requiresAuth) {
        const hasToken = authStore.token || sessionStorage.getItem('auth_token')
        const hasUser = authStore.user || sessionStorage.getItem('user')
        const isAuth = !!(hasToken && hasUser)

        if (!isAuth) {
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
