<template>
  <aside class="sidebar">
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
          v-for="item in navigation.main" 
          :key="item.id"
          :class="['nav-item', { active: activeNav === item.id }]"
          @click="$emit('navigate', item.id)"
        >
          <component :is="item.icon" :size="20" :stroke-width="2" class="nav-icon" />
          <span>{{ item.label }}</span>
        </div>
      </div>

      <div class="nav-section">
        <div class="nav-section-title">Çalışma Alanı</div>
        <div 
          v-for="item in navigation.workspace" 
          :key="item.id"
          :class="['nav-item', { active: activeNav === item.id }]"
          @click="$emit('navigate', item.id)"
        >
          <component :is="item.icon" :size="20" :stroke-width="2" class="nav-icon" />
          <span>{{ item.label }}</span>
        </div>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="user-profile">
        <div class="user-avatar">{{ userInitials }}</div>
        <div class="user-info">
          <div class="user-name">{{ user.name }}</div>
          <div class="user-role">{{ user.role }}</div>
        </div>
        <MoreVertical :size="16" :stroke-width="2" />
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { 
  Layers, 
  LayoutDashboard, 
  TrendingUp, 
  FolderKanban, 
  Users, 
  FileText, 
  Calendar, 
  Settings,
  MoreVertical 
} from 'lucide-vue-next'

const props = defineProps({
  activeNav: {
    type: String,
    default: 'dashboard'
  },
  user: {
    type: Object,
    default: () => ({
      name: 'Ahmet Yılmaz',
      role: 'Executive Director'
    })
  }
})

defineEmits(['navigate'])

const navigation = {
  main: [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analytics', label: 'Analitik', icon: TrendingUp },
    { id: 'projects', label: 'Projeler', icon: FolderKanban },
    { id: 'team', label: 'Ekip', icon: Users }
  ],
  workspace: [
    { id: 'documents', label: 'Dökümanlar', icon: FileText },
    { id: 'calendar', label: 'Takvim', icon: Calendar },
    { id: 'settings', label: 'Ayarlar', icon: Settings }
  ]
}

const userInitials = computed(() => {
  return props.user.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
})
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: var(--obsidian-black);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
  animation: slideInLeft var(--transition-slow) ease-out;
}

.sidebar::after {
  content: '';
  position: absolute;
  top: 0;
  right: -1px;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, 
    transparent 0%, 
    var(--indigo-glow) 50%, 
    transparent 100%);
  pointer-events: none;
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
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 24px var(--indigo-glow-strong);
  animation: glow 3s ease-in-out infinite;
}

.logo-image {
  width: 24px;
  height: 24px;
  object-fit: contain;
  color: white;
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
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: var(--letter-spacing-normal);
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
              0 0 16px var(--indigo-glow);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--indigo-primary);
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 12px var(--indigo-primary);
}

.nav-icon {
  flex-shrink: 0;
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
  border-radius: var(--radius-sm);
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
  background: linear-gradient(135deg, var(--indigo-primary), #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 0 16px var(--indigo-glow);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-normal);
  line-height: var(--line-height-tight);
}

.user-role {
  font-size: 12px;
  color: var(--text-muted);
  letter-spacing: var(--letter-spacing-normal);
}
</style>
