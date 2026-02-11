<template>
  <div class="dashboard-layout" :class="`sector-${sector}`">
    <!-- Header -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="brand-section">
          <div class="sector-icon-wrapper">
            <component :is="sectorIcon" :size="28" :stroke-width="2" />
          </div>
          <div>
            <h1 class="title">{{ sectorName }}</h1>
            <p class="subtitle">Premium {{ sectorName }} Management System</p>
          </div>
        </div>
        <div class="header-actions">
          <button class="btn-icon" @click="toggleNotifications" title="Bildirimler">
            <Bell :size="20" :stroke-width="2" />
            <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
          </button>
          <button class="btn-icon" @click="$router.push('/settings')" title="Ayarlar">
            <Settings :size="20" :stroke-width="2" />
          </button>
          <button class="btn-icon" @click="logout" title="Çıkış">
            <LogOut :size="20" :stroke-width="2" />
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="dashboard-main">
      <slot></slot>
    </main>

    <!-- Notification Panel -->
    <Transition name="slide-left">
      <div v-if="showNotifications" class="notification-panel">
        <div class="panel-header">
          <h3>Bildirimler</h3>
          <button @click="toggleNotifications" class="close-btn">
            <X :size="20" />
          </button>
        </div>
        <div class="panel-content">
          <div v-if="notifications.length === 0" class="empty-state">
            <Bell :size="48" :stroke-width="1.5" />
            <p>Bildirim bulunmuyor</p>
          </div>
          <div v-else class="notification-list">
            <div 
              v-for="notif in notifications" 
              :key="notif.id"
              class="notification-item"
              :class="{ unread: !notif.read }"
            >
              <div class="notif-icon" :style="{ background: notif.color }">
                <component :is="notif.icon" :size="16" />
              </div>
              <div class="notif-content">
                <p class="notif-title">{{ notif.title }}</p>
                <p class="notif-message">{{ notif.message }}</p>
                <span class="notif-time">{{ notif.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Overlay -->
    <Transition name="fade">
      <div v-if="showNotifications" class="overlay" @click="toggleNotifications"></div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Bell, Settings, LogOut, X, Activity, Calendar, AlertCircle } from 'lucide-vue-next'
import { useSectorTheme } from '../../composables/useSectorTheme'
import { useAuthStore } from '../../stores/auth'

const props = defineProps({
  sector: {
    type: String,
    required: true
  },
  sectorIcon: {
    type: Object,
    default: () => Activity
  }
})

const router = useRouter()
const authStore = useAuthStore()
const { theme, applyTheme } = useSectorTheme(props.sector)

const showNotifications = ref(false)
const unreadCount = ref(3)
const notifications = ref([
  {
    id: 1,
    icon: Calendar,
    color: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    title: 'Yeni Randevu',
    message: 'Bugün saat 14:00 için yeni randevu oluşturuldu',
    time: '5 dakika önce',
    read: false
  },
  {
    id: 2,
    icon: AlertCircle,
    color: 'linear-gradient(135deg, #f59e0b, #fbbf24)',
    title: 'Sistem Güncellemesi',
    message: 'Yeni özellikler eklendi, kontrol edin',
    time: '1 saat önce',
    read: false
  },
  {
    id: 3,
    icon: Activity,
    color: 'linear-gradient(135deg, #10b981, #34d399)',
    title: 'Performans Raporu',
    message: 'Haftalık performans raporu hazır',
    time: '2 saat önce',
    read: true
  }
])

const sectorName = computed(() => theme.value.name)

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    unreadCount.value = 0
  }
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  applyTheme()
})
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background: #030712;
  color: white;
  font-family: 'Inter', sans-serif;
}

/* Header */
.dashboard-header {
  background: rgba(3, 7, 18, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 20px 32px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-content {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.sector-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--sector-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 0 24px var(--sector-glow);
}

.title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 13px;
  color: #9ca3af;
  margin: 4px 0 0 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-color: rgba(255, 255, 255, 0.15);
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: white;
  font-size: 11px;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #030712;
}

/* Main Content */
.dashboard-main {
  max-width: 1600px;
  margin: 0 auto;
  padding: 32px;
}

/* Notification Panel */
.notification-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background: rgba(17, 24, 39, 0.95);
  backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: #9ca3af;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 32px;
  color: #6b7280;
  text-align: center;
}

.empty-state p {
  margin-top: 16px;
  font-size: 14px;
}

.notification-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 12px;
  transition: all 0.2s;
  cursor: pointer;
}

.notification-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.1);
}

.notification-item.unread {
  border-color: var(--sector-accent);
  background: var(--sector-bg);
}

.notif-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-title {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: white;
}

.notif-message {
  font-size: 13px;
  color: #9ca3af;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.notif-time {
  font-size: 11px;
  color: #6b7280;
}

/* Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 90;
}

/* Transitions */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-left-enter-from {
  transform: translateX(100%);
}

.slide-left-leave-to {
  transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard-main {
    padding: 20px 16px;
  }

  .notification-panel {
    width: 100%;
  }

  .dashboard-header {
    padding: 16px 20px;
  }

  .brand-section {
    gap: 12px;
  }

  .sector-icon-wrapper {
    width: 40px;
    height: 40px;
  }

  .title {
    font-size: 18px;
  }

  .subtitle {
    font-size: 12px;
  }
}
</style>
