<template>
  <div class="executive-shell">
    <!-- Sector-Adaptive Sidebar -->
    <aside class="shell-sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon" ref="logoIcon">
            <component :is="currentLogoIcon" :size="20" :stroke-width="2" />
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

      <div class="sidebar-footer">
        <div class="user-profile">
          <div class="user-avatar" ref="userAvatar">AY</div>
          <div class="user-info">
            <div class="user-name">Ahmet Yılmaz</div>
            <div class="user-role">Executive Director</div>
          </div>
          <MoreVertical :size="16" :stroke-width="2" />
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="shell-main">
      <!-- Sector-Adaptive Topbar -->
      <header class="shell-topbar">
        <div class="topbar-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
          <div class="sector-badge" ref="sectorBadge">
            <component :is="currentSectorIcon" :size="14" :stroke-width="2.5" />
            <span>{{ sectorStore.config?.displayName || sectorStore.currentSector || 'Medical' }}</span>
          </div>
        </div>

        <div class="topbar-right">
          <!-- Sector is now auto-detected from login, no manual switching -->
          <div class="topbar-actions">
            <button class="action-btn">
              <Bell :size="18" :stroke-width="2" />
            </button>
            <button class="action-btn">
              <Search :size="18" :stroke-width="2" />
            </button>
          </div>
        </div>
      </header>

      <!-- Content Area with Transition -->
      <div class="shell-content">
        <Transition name="fade-slide" mode="out-in">
             <component 
                :is="activeComponent" 
                v-bind="activeComponentProps"
                :key="activeNav"
            />
        </Transition>
      </div>
    </main>

    <!-- Pulse Center -->
    <PulseCenter />
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, inject } from 'vue'
import { 
  Activity, Stethoscope, Scale, Building2, Home, Gavel,
  LayoutDashboard, TrendingUp, FolderKanban, Users, 
  FileText, Calendar, Settings, MoreVertical, Bell, Search,
  Briefcase, Target, ArrowRight, CalendarCheck, User, UserCheck,
  Phone, Heart
} from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import PulseCenter from './PulseCenter.vue'
import DashboardContent from './dashboard/DashboardContent.vue'
import CallCenterDashboard from './CallCenterDashboard.vue'
import SatisfactionDashboard from './SatisfactionDashboard.vue'
import PlaceholderView from './dashboard/PlaceholderView.vue'
import gsap from 'gsap'

const sectorStore = useSectorStore()
const axios = inject('axios')

// State
const activeNav = ref('dashboard')

// Current sector icon (based on auto-detected sector from login)
const currentSectorIcon = computed(() => {
  const iconMap = {
    medical: Stethoscope,
    legal: Scale,
    real_estate: Building2
  }
  return iconMap[sectorStore.currentSector]
})

const currentLogoIcon = computed(() => {
  const iconMap = {
    medical: Activity,
    legal: Scale,
    real_estate: Home
  }
  return iconMap[sectorStore.currentSector]
})

// Navigation items
const mainNavigation = computed(() => {
  const baseNav = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'callcenter', label: 'Call Center', icon: Phone },
    { id: 'satisfaction', label: 'Memnuniyet', icon: Heart },
    { id: 'analytics', label: 'Analitik', icon: TrendingUp }
  ]
  
  // Add sector-specific items
  if (sectorStore.currentSector === 'medical') {
    baseNav.push({ id: 'appointments', label: 'Randevular', icon: CalendarCheck })
  } else if (sectorStore.currentSector === 'legal') {
    baseNav.push({ id: 'cases', label: 'Dosyalar', icon: Briefcase })
  } else if (sectorStore.currentSector === 'real_estate') {
    baseNav.push({ id: 'properties', label: 'Emlaklar', icon: Home })
  }
  
  return baseNav
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

// Dynamic Component Resolution
const activeComponent = computed(() => {
    if (activeNav.value === 'dashboard') return DashboardContent
    if (activeNav.value === 'callcenter') return CallCenterDashboard
    if (activeNav.value === 'satisfaction') return SatisfactionDashboard
    return PlaceholderView
})

// Props passed to the active component
const activeComponentProps = computed(() => {
    if (activeNav.value === 'dashboard') return {}
    
    // For placeholders, pass title and icon
    const item = [...mainNavigation.value, ...workspaceNavigation.value].find(i => i.id === activeNav.value)
    return {
        title: item ? item.label : 'Modül',
        icon: item ? item.icon : Activity
    }
})

// Refs for GSAP animations
const logoIcon = ref(null)
const userAvatar = ref(null)
const sectorBadge = ref(null)

// Methods
const handleNavigate = (navId) => {
  activeNav.value = navId
}

// Sector is auto-set from login, no manual switching needed
</script>

<style scoped>
.executive-shell {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: var(--obsidian-black);
  overflow: hidden;
}

/* Sidebar */
.shell-sidebar {
  width: 280px;
  background: var(--obsidian-black);
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
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--current-accent), var(--current-accent));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px var(--current-glow-strong);
  transition: all var(--transition-slow);
  color: #ffffff;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-tight);
  background: linear-gradient(135deg, #ffffff, #a1a1aa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
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
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: var(--text-muted);
}

/* Main Content */
.shell-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.shell-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--obsidian-black);
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

.sector-switcher {
  display: flex;
  gap: 8px;
  padding: 4px;
  background: var(--surface-elevated);
  border-radius: 12px;
  border: 1px solid var(--border-subtle);
}

.sector-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.sector-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.sector-btn.active {
  background: var(--current-glow);
  color: var(--current-accent);
  box-shadow: 0 0 12px var(--current-glow);
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

/* Content Area */
.shell-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  background: var(--obsidian-black);
  width: 100%;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .shell-sidebar {
    width: 240px;
  }
  
  .shell-content {
    padding: 24px;
  }
  
  .shell-topbar {
    padding: 16px 24px;
  }
  
  .sector-switcher {
    display: none; /* Hide on tablet */
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
    display: none; /* Hide user profile on mobile */
  }
  
  .shell-content {
    padding: 16px;
  }
  
  .shell-topbar {
    padding: 12px 16px;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .topbar-left {
    flex: 1;
    min-width: 0;
  }
  
  .page-title {
    font-size: 18px;
  }
  
  .topbar-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .sector-switcher {
    display: flex;
    flex: 1;
    justify-content: center;
  }
  
  .sector-btn span {
    display: none; /* Hide text, show only icons on mobile */
  }
}

@media (max-width: 480px) {
  .shell-content {
    padding: 12px;
  }
  
  .page-title {
    font-size: 16px;
  }
  
  .sector-badge {
    font-size: 10px;
    padding: 4px 8px;
  }
  
  .sector-badge span {
    display: none; /* Hide text on very small screens */
  }
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
</style>
