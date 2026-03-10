<template>
  <div class="executive-shell">
    <!-- Sidebar Pillar -->
    <aside class="shell-sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <img src="/logo.svg" alt="NextGent Logo" class="logo-image" />
          </div>
          <span class="logo-text">NextGent</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">Ana Menü</div>
          <div 
            v-for="item in mainNavigation" 
            :key="item.id"
            :class="['nav-item', { active: activeNav === item.id }]"
            @click="handleNavigate(item.id)"
          >
            <component :is="item.icon" :size="20" :stroke-width="2" class="nav-icon" />
            <span>{{ item.label }}</span>
          </div>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">Çalışma Alanı</div>
          <div 
            v-for="item in workspaceNavigation" 
            :key="item.id"
            :class="['nav-item', { active: activeNav === item.id }]"
            @click="handleNavigate(item.id)"
          >
            <component :is="item.icon" :size="20" :stroke-width="2" class="nav-icon" />
            <span>{{ item.label }}</span>
          </div>
        </div>
      </nav>

      <div class="sidebar-footer" ref="footerRef">
        <div class="user-profile" @click.stop="toggleUserMenu">
          <div class="user-avatar" ref="userAvatar">{{ userInitials }}</div>
          <div class="user-info">
            <div class="user-name">{{ userName }}</div>
            <div class="user-role">{{ userRole }}</div>
          </div>
          <MoreVertical :size="16" :stroke-width="2" />
        </div>
        <div v-if="showUserMenu" class="user-menu-panel" @click.stop>
          <div class="profile-header">
            <div class="profile-avatar" :style="{ background: `linear-gradient(135deg, var(--current-accent), var(--current-accent))` }">{{ userInitials }}</div>
            <div class="profile-info">
              <div class="profile-name">{{ userName }}</div>
              <div class="profile-role">{{ userRole }}</div>
            </div>
          </div>
          <div class="profile-details">
            <div class="detail-row">
              <span class="detail-label">Müşteri ID</span>
              <span class="detail-value">{{ authStore.user?.customer_id || '-' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Sektör</span>
              <span class="detail-value">{{ sectorStore.currentSector?.label || 'Genel' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Segment</span>
              <span class="detail-value">{{ authStore.user?.segment || 'Standart' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">E-posta</span>
              <span class="detail-value">{{ authStore.user?.email || '-' }}</span>
            </div>
          </div>
          <div class="profile-actions">
            <button class="profile-action-btn" @click="handleNavigate('settings'); showUserMenu = false">
              <Settings :size="16" :stroke-width="2" />
              <span>Ayarlar</span>
            </button>
            <button class="profile-action-btn logout" @click="handleLogout">
              <LogOut :size="16" :stroke-width="2" />
              <span>Çıkış Yap</span>
            </button>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="shell-main">
      <!-- Topbar -->
      <header class="shell-topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
          <div class="sector-badge" ref="sectorBadge" v-if="isCustomer">
            <component :is="currentSectorIcon" :size="14" :stroke-width="2.5" />
            <span>{{ sectorStore.currentSector?.label || 'Genel Bakış' }}</span>
          </div>
        </div>

        <div class="topbar-right">
          <div class="topbar-actions">
            <button class="action-btn" @click="handleNotifications">
              <Bell :size="18" :stroke-width="2" />
            </button>
            <div class="search-container" :class="{ active: isSearchActive }">
              <input 
                v-if="isSearchActive"
                ref="searchInput"
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                @blur="handleSearchBlur"
                type="text" 
                placeholder="Müşteri veya İşlem Ara..." 
                class="search-input"
              />
              <button class="action-btn" @click="toggleSearch">
                <Search :size="18" :stroke-width="2" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Content Area: nested routes render here -->
      <div class="shell-content">
        <Transition name="fade-slide" mode="out-in">
          <router-view :key="route.path" @navigate="handleNavigate" />
        </Transition>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, watchEffect, nextTick, onMounted, onUnmounted, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Activity, Stethoscope, Scale, Building2, Home, Gavel,
  LayoutDashboard, TrendingUp, FolderKanban, Users, 
  FileText, Calendar, Settings, MoreVertical, Bell, Search,
  Briefcase, Target, ArrowRight, CalendarCheck, User, UserCheck,
  Phone, Heart, ShoppingBag, Factory, GraduationCap, Car,
  Landmark, Coffee, ShoppingCart, LogOut, Sparkles
} from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import { useNotificationStore } from '../stores/notification'
import { useAuthStore } from '../stores/auth'
import { useAdminStore } from '../stores/admin'

const sectorStore = useSectorStore()
const notificationStore = useNotificationStore()
const authStore = useAuthStore()
const adminStore = useAdminStore()
const axios = inject('axios')
const router = useRouter()
const route = useRoute()

// Dynamic user info
const userName = computed(() => {
    const u = authStore.user
    if (!u) return 'Kullanıcı'
    return u.first_name && u.last_name ? `${u.first_name} ${u.last_name}` : u.name || u.customer_id || 'Kullanıcı'
})

const userInitials = computed(() => {
    const name = userName.value
    const parts = name.split(' ')
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
    return name.substring(0, 2).toUpperCase()
})

const userRole = computed(() => {
    const u = authStore.user
    if (!u) return 'Müşteri'
    return u.role === 'admin' ? 'Yönetici' : sectorStore.currentSector?.label || 'Müşteri'
})

const showUserMenu = ref(false)
const footerRef = ref(null)

const toggleUserMenu = () => { showUserMenu.value = !showUserMenu.value }

const handleLogout = () => {
    authStore.logout()
    showUserMenu.value = false
    router.push('/login')
}

// Click outside to close user menu
const handleClickOutside = (e) => {
    if (footerRef.value && !footerRef.value.contains(e.target)) {
        showUserMenu.value = false
    }
}

// Nav id from current route (for sidebar highlight)
const activeNav = computed(() => {
  const p = route.path
  if (p === '/dashboard' || p === '/dashboard/portal' || p.startsWith('/dashboard/sectors/')) return 'dashboard'
  if (p === '/dashboard/appointments') return 'appointments'
  if (p === '/dashboard/messages') return 'messages'
  if (p === '/dashboard/calls') return 'calls'
  if (p === '/dashboard/satisfaction') return 'satisfaction'
  if (p === '/dashboard/documents') return 'documents'
  if (p === '/dashboard/calendar') return 'calendar'
  if (p === '/dashboard/settings') return 'settings'
  if (p === '/dashboard/admin-dashboard') return 'dashboard'
  if (p === '/dashboard/users') return 'users'
  if (p === '/dashboard/cards') return 'cards'
  if (p === '/dashboard/flows') return 'flows'
  if (p === '/dashboard/audits') return 'audits'
  if (p === '/dashboard/analytics') return 'analytics'
  return 'dashboard'
})

// Current sector icon (based on auto-detected sector from login)
const currentSectorIcon = computed(() => {
  if (!sectorStore || !sectorStore.currentSectorId) return Activity
  const iconMap = {
    medical: Stethoscope,
    legal: Scale,
    real_estate: Building2,
    retail: ShoppingBag,
    manufacturing: Factory,
    education: GraduationCap,
    automotive: Car,
    finance: Landmark,
    hospitality: Coffee,
    ecommerce: ShoppingCart,
    beauty: Sparkles
  }
  return iconMap[sectorStore.currentSectorId] || Activity
})

// Current logo icon
const currentLogoIcon = computed(() => {
  const iconMap = {
    medical: Activity,
    legal: Scale,
    real_estate: Home,
    retail: ShoppingBag,
    manufacturing: Factory,
    education: GraduationCap,
    automotive: Car,
    finance: Landmark,
    hospitality: Coffee,
    ecommerce: ShoppingCart,
    beauty: Sparkles
  }
  return iconMap[sectorStore.currentSectorId] || Activity
})

// Helper to check if user is customer (resilient to store hydration timing)
const isCustomer = computed(() => {
    const isAdmin = authStore.user?.role === 'admin'
    const hasAdminSession = adminStore?.isAuthenticated ?? false
    if (authStore.user && !isAdmin) return true
    // Fallback: token exists and not admin session -> treat as customer (handles hydration delay)
    if (authStore.token && !hasAdminSession) return true
    // Route fallback: /dashboard is customer shell (admin uses /admin/dashboard)
    if (route.path === '/dashboard' && authStore.token) return true
    return false
})

// Navigation items
const mainNavigation = computed(() => {
  // Safe sector check
  const sectorName = sectorStore?.currentSectorId || 'medical'
  
  // Customer Navigation (Restore original)
  if (isCustomer.value) {
      return [
        { id: 'dashboard', label: sectorStore.t('dashboard'), icon: LayoutDashboard },
        { id: 'appointments', label: sectorStore.t('appointments'), icon: CalendarCheck },
        { id: 'messages', label: sectorStore.t('messages'), icon: Briefcase },
        { id: 'calls', label: sectorStore.t('calls'), icon: Phone },
        { id: 'satisfaction', label: sectorStore.t('satisfaction'), icon: Heart }
      ]
  }

  // Admin Navigation (Classic)
  return [
    { id: 'dashboard', label: sectorStore.t('admin_dashboard'), icon: LayoutDashboard },
    { id: 'users', label: sectorStore.t('users'), icon: Users },
    { id: 'cards', label: sectorStore.t('cards'), icon: FileText }, // Using FileText as credit card placeholder
    { id: 'flows', label: sectorStore.t('flows'), icon: Activity },
    { id: 'audits', label: sectorStore.t('audits'), icon: FileText },
    { id: 'analytics', label: sectorStore.t('analytics'), icon: TrendingUp }
  ]
})

const workspaceNavigation = computed(() => [
  { id: 'documents', label: sectorStore.t('documents'), icon: FileText },
  { id: 'calendar', label: sectorStore.t('calendar'), icon: Calendar },
  { id: 'settings', label: sectorStore.t('settings'), icon: Settings }
])

const currentPageTitle = computed(() => {
  const item = [...mainNavigation.value, ...workspaceNavigation.value]
    .find(nav => nav.id === activeNav.value)
  return item ? item.label : sectorStore.t('dashboard')
})


// Refs for GSAP animations
const logoIcon = ref(null)
const userAvatar = ref(null)
const sectorBadge = ref(null)

// Nav id → dashboard path (nested routes)
const navIdToPath = (navId) => {
  const base = '/dashboard'
  if (navId === 'dashboard') return isCustomer.value ? base : base + '/admin-dashboard'
  const map = {
    appointments: '/appointments',
    messages: '/messages',
    calls: '/calls',
    satisfaction: '/satisfaction',
    documents: '/documents',
    calendar: '/calendar',
    settings: '/settings',
    users: '/users',
    cards: '/cards',
    flows: '/flows',
    audits: '/audits',
    analytics: '/analytics'
  }
  const sub = map[navId]
  return sub ? base + sub : base
}

const isNavigating = ref(false)
const handleNavigate = (navId) => {
  if (isNavigating.value) return
  if (activeNav.value === navId) return
  isNavigating.value = true
  const path = navIdToPath(navId)
  router.push(path).finally(() => { isNavigating.value = false })
}

// Search Logic
const isSearchActive = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)

const toggleSearch = () => {
  isSearchActive.value = !isSearchActive.value
  if (isSearchActive.value) {
    nextTick(() => {
      searchInput.value.focus()
    })
  }
}

const handleNotifications = () => {
  // Toggle notification panel (implementation pending sidebar)
  notificationStore.info('Bildirim paneli sağda açıldı (Simülasyon)', 'Bildirimler')
}

const handleSearch = () => {
  const query = searchQuery.value.toLowerCase()
  if (!query) return

  if (query.includes('randevu') || query.includes('takvim') || query.includes('calendar')) {
    router.push('/dashboard/calendar')
    notificationStore.success('Takvime yönlendirildi', 'Arama')
  } else if (query.includes('belge') || query.includes('rapor') || query.includes('dosya')) {
    router.push('/dashboard/documents')
    notificationStore.success('Belgelere yönlendirildi', 'Arama')
  } else if (query.includes('analiz') || query.includes('grafik') || query.includes('kpi')) {
    router.push('/dashboard/analytics')
    notificationStore.success('Analitik sayfasına yönlendirildi', 'Arama')
  } else if (query.includes('ayar') || query.includes('profil')) {
    router.push('/dashboard/settings')
    notificationStore.success('Ayarlara yönlendirildi', 'Arama')
  } else {
    notificationStore.info(`"${searchQuery.value}" için sonuç bulunamadı.`, 'Arama')
  }

  isSearchActive.value = false
  searchQuery.value = ''
}

const handleSearchBlur = () => {
  // Optional: Auto-close on blur if empty
  if (!searchQuery.value) {
    isSearchActive.value = false
  }
}

// Sector is auto-set from login, no manual switching needed

// Dynamic Sector Theme → CSS Variables
// Keeps --current-accent, --current-glow etc in sync with sectorStore globally,
// so CalendarView, DocumentsView, SettingsView etc all pick up the sector color.
const applyThemeVars = () => {
    const theme = sectorStore.theme
    if (!theme) return
    const root = document.documentElement
    root.style.setProperty('--current-accent', theme.primary || '#6366f1')
    root.style.setProperty('--current-glow', (theme.primary || '#6366f1') + '26')   // ~15% opacity
    root.style.setProperty('--current-glow-strong', (theme.primary || '#6366f1') + '40') // ~25% opacity
    // RGB for rgba() usage
    const hex = (theme.primary || '#6366f1').replace('#', '')
    const r = parseInt(hex.substring(0, 2), 16)
    const g = parseInt(hex.substring(2, 4), 16)
    const b = parseInt(hex.substring(4, 6), 16)
    root.style.setProperty('--current-rgb', `${r}, ${g}, ${b}`)
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)
    applyThemeVars()
})

// Re-apply whenever sector changes
watch(() => sectorStore.currentSectorId, () => {
    applyThemeVars()
}, { immediate: true })

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.executive-shell {
  display: flex;
  height: 100dvh;
  width: 100vw;
  background: var(--bg-main);
  overflow: hidden;
}

/* Sidebar */
.shell-sidebar {
  width: 280px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
}

.shell-sidebar::after {
  content: '';
  position: absolute;
  top: 0;
  right: -1px;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, 
    transparent 0%, 
    var(--current-glow-strong) 50%, 
    transparent 100%);
  pointer-events: none;
  transition: background var(--transition-slow);
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-slow);
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
  color: var(--text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  padding: 0 12px 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
  position: relative;
}

.nav-item:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--surface-elevated);
  color: var(--text-primary);
  box-shadow: inset 0 0 0 1px var(--border-hover),
              0 0 16px var(--current-glow);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--current-accent);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 12px var(--current-accent);
  transition: background var(--transition-slow);
}

.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid var(--border-subtle);
  position: relative;
  z-index: 1001; /* Ensure user menu is on top */
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--surface-elevated);
}

.user-profile:hover {
  background: var(--surface-hover);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--current-accent), var(--current-accent));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 0 16px var(--current-glow);
  transition: all var(--transition-slow);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: var(--text-muted);
}

.more-icon {
  color: var(--text-muted);
  transition: transform var(--transition-fast), color var(--transition-fast);
  flex-shrink: 0;
}

.more-icon.menu-open {
  transform: rotate(90deg);
  color: var(--current-accent);
}

/* Main Content */
.shell-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  width: 100%;
}

.shell-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-sidebar);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
}

.sector-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--current-glow);
  border: 1px solid var(--current-accent);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--current-accent);
  transition: all var(--transition-slow);
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.topbar-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

/* Search Bar Expansion */
.search-container {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.search-input {
  width: 0;
  opacity: 0;
  padding: 0;
  border: none;
  background: var(--surface-elevated);
  color: var(--text-primary);
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 40px;
  font-size: 14px;
}

.search-container.active .search-input {
  width: 240px;
  opacity: 1;
  padding: 0 12px;
  border: 1px solid var(--border-subtle);
}

.search-input:focus {
  outline: none;
  border-color: var(--current-accent);
  box-shadow: 0 0 0 2px var(--current-glow);
}

/* Content Area */
.shell-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.dashboard-loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
  color: var(--text-secondary);
}
.dashboard-loading-state p {
  font-size: 14px;
  font-weight: 500;
}
.loading-spinner-small {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--current-accent);
  border-radius: 50%;
  animation: shell-spin 0.8s linear infinite;
}
@keyframes shell-spin {
  to { transform: rotate(360deg); }
  background: #030303;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Global Heading Fixes for Dashboard Items */
:deep(h3) {
  color: var(--text-primary) !important;
}

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .shell-sidebar {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .executive-shell {
    flex-direction: column;
  }
  
  .shell-sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 1px solid var(--border-subtle);
  }
  
  .sidebar-nav {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 12px;
  }
  
  .nav-section {
    margin-bottom: 0;
    display: flex;
    gap: 8px;
  }
  
  .nav-section-title {
    display: none;
  }
  
  .nav-item {
    white-space: nowrap;
    min-width: fit-content;
  }
  
  .sidebar-footer {
    display: none;
  }
  
  .shell-topbar {
    padding: 12px 16px;
    flex-wrap: wrap;
    gap: 12px;
  }
}

.user-menu-panel {
  position: absolute;
  bottom: 100%;
  left: 12px;
  right: 12px;
  margin-bottom: 8px;
  background: var(--bg-surface);
  backdrop-filter: blur(24px);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  box-shadow: 0 -20px 50px rgba(0, 0, 0, 0.2), 0 0 0 1px var(--border-subtle) inset;
  overflow: hidden;
  z-index: 100;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.profile-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: #fff;
  box-shadow: 0 0 20px var(--current-glow);
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.profile-role {
  font-size: 12px;
  color: var(--current-accent);
  font-weight: 500;
}

.profile-details {
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-label {
  font-size: 12px;
  color: #71717a;
  font-weight: 500;
}

.detail-value {
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 500;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-actions {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #d4d4d8;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.profile-action-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.profile-action-btn.logout {
  color: #f87171;
}

.profile-action-btn.logout:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
}
</style>
