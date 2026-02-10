<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="admin-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <Shield :size="24" :stroke-width="2.5" />
          </div>
          <span class="logo-text" v-if="!sidebarCollapsed">NextGent Admin</span>
        </div>
        <button class="collapse-btn" @click="toggleSidebar">
          <ChevronLeft :size="20" v-if="!sidebarCollapsed" />
          <ChevronRight :size="20" v-else />
        </button>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <component :is="item.icon" :size="20" :stroke-width="2" />
          <span class="nav-text" v-if="!sidebarCollapsed">{{ item.label }}</span>
          <span class="nav-badge" v-if="item.badge && !sidebarCollapsed">{{ item.badge }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="logout-btn" @click="handleLogout">
          <LogOut :size="20" :stroke-width="2" />
          <span v-if="!sidebarCollapsed">Çıkış Yap</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="admin-main">
      <!-- Header -->
      <header class="admin-header">
        <div class="header-left">
          <h1 class="page-title">{{ pageTitle }}</h1>
          <p class="page-subtitle">{{ pageSubtitle }}</p>
        </div>
        <div class="header-right">
          <button class="header-btn">
            <Bell :size="20" :stroke-width="2" />
            <span class="notification-dot"></span>
          </button>
          <button class="header-btn">
            <Settings :size="20" :stroke-width="2" />
          </button>
          <div class="user-menu">
            <div class="user-avatar">
              <User :size="20" :stroke-width="2" />
            </div>
            <div class="user-info">
              <span class="user-name">{{ adminStore.user?.username || 'Admin' }}</span>
              <span class="user-role">{{ adminStore.user?.role || 'Super Admin' }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '../stores/admin'
import {
  Shield,
  LayoutDashboard,
  Users,
  CreditCard,
  Workflow,
  FileText,
  BarChart3,
  Settings,
  Bell,
  User,
  LogOut,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const adminStore = useAdminStore()

const sidebarCollapsed = ref(false)

const menuItems = [
  { path: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/admin/users', label: 'Kullanıcılar', icon: Users, badge: '24' },
  { path: '/admin/cards', label: 'Kartlar', icon: CreditCard },
  { path: '/admin/flow', label: 'Akış Motoru', icon: Workflow },
  { path: '/admin/logs', label: 'Audit Logları', icon: FileText },
  { path: '/admin/analytics', label: 'Analitik', icon: BarChart3 }
]

const pageTitle = computed(() => {
  const currentItem = menuItems.find(item => item.path === route.path)
  return currentItem?.label || 'Dashboard'
})

const pageSubtitle = computed(() => {
  const subtitles = {
    '/admin/dashboard': 'Sistem performansı ve istatistikler',
    '/admin/users': 'Kullanıcı yönetimi ve izinler',
    '/admin/cards': 'Kart şablonları ve içerik yönetimi',
    '/admin/flow': 'Otomasyon akışları ve kurallar',
    '/admin/logs': 'Sistem aktivite kayıtları',
    '/admin/analytics': 'Token kullanımı ve maliyet analizi'
  }
  return subtitles[route.path] || ''
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const isActive = (path) => {
  return route.path === path
}

const handleLogout = async () => {
  await adminStore.logout()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100vw !important;
  max-width: none !important;
  background: var(--background);
  overflow: hidden;
}

/* Sidebar */
.admin-sidebar {
  width: 280px;
  background: var(--surface-elevated);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 100;
}

.admin-sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: 20px 12px;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 10px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
  white-space: nowrap;
}

.nav-item:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  color: var(--indigo-primary);
  font-weight: 600;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 60%;
  background: var(--indigo-primary);
  border-radius: 0 3px 3px 0;
}

.nav-text {
  flex: 1;
  font-size: 14px;
  letter-spacing: -0.01em;
}

.nav-badge {
  padding: 2px 8px;
  background: var(--indigo-primary);
  color: white;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.sidebar-footer {
  padding: 20px 12px;
  border-top: 1px solid var(--border-subtle);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  font-weight: 500;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

/* Main Content */
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 100% !important;
  max-width: none !important;
  min-width: 0;
}

.admin-header {
  height: 80px;
  background: var(--surface-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 40px; /* Increased padding slightly but kept wide */
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  width: 100% !important;
  max-width: none !important;
}

.header-left {
  flex: 1;
  min-width: 0;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.header-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid var(--surface-elevated);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-menu:hover {
  border-color: var(--border-hover);
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.user-role {
  font-size: 12px;
  color: var(--text-secondary);
}

.admin-content {
  flex: 1;
  overflow-y: auto;
  background: var(--background);
  width: 100% !important;
  max-width: none !important;
  display: flex;
  flex-direction: column;
}

/* Scrollbar */
.sidebar-nav::-webkit-scrollbar,
.admin-content::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track,
.admin-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb,
.admin-content::-webkit-scrollbar-thumb {
  background: var(--border-subtle);
  border-radius: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover,
.admin-content::-webkit-scrollbar-thumb:hover {
  background: var(--border-hover);
}

/* Responsive */
@media (max-width: 1024px) {
  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1000;
  }

  .admin-sidebar.collapsed {
    transform: translateX(-100%);
  }
}
</style>
