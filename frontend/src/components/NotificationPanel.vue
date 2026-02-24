<template>
  <Transition name="dropdown-fade">
    <div v-if="isOpen" class="notification-dropdown" v-click-outside="closePanel">
      <!-- Header -->
      <div class="dropdown-header">
        <div class="header-content">
          <Bell :size="18" :stroke-width="2" />
          <h3>Bildirimler</h3>
          <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
        </div>
        <div class="header-actions">
          <button 
            v-if="notifications.length > 0" 
            @click="markAllAsRead" 
            class="action-btn"
            title="Tümünü okundu işaretle"
          >
            <CheckCheck :size="16" :stroke-width="2" />
          </button>
          <button 
            v-if="notifications.length > 0" 
            @click="clearAll" 
            class="action-btn"
            title="Tümünü temizle"
          >
            <Trash2 :size="16" :stroke-width="2" />
          </button>
        </div>
      </div>

      <!-- Notifications List -->
      <div class="notifications-list">
        <div v-if="notifications.length === 0" class="empty-state">
          <BellOff :size="32" :stroke-width="1.5" />
          <p>Bildirim yok</p>
        </div>

        <TransitionGroup name="notification-item" tag="div">
          <div
            v-for="notification in displayedNotifications"
            :key="notification.id"
            :class="['notification-item', notification.type, { unread: !notification.read }]"
            @click="handleNotificationClick(notification)"
          >
            <div class="notification-icon">
              <Info v-if="notification.type === 'info'" :size="16" :stroke-width="2" />
              <CheckCircle v-else-if="notification.type === 'success'" :size="16" :stroke-width="2" />
              <AlertTriangle v-else-if="notification.type === 'warning'" :size="16" :stroke-width="2" />
              <AlertCircle v-else-if="notification.type === 'error'" :size="16" :stroke-width="2" />
            </div>
            
            <div class="notification-content">
              <h4>{{ notification.title }}</h4>
              <p>{{ notification.message }}</p>
              <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
            </div>

            <button 
              @click.stop="removeNotification(notification.id)" 
              class="remove-btn"
              title="Kaldır"
            >
              <X :size="14" :stroke-width="2" />
            </button>
          </div>
        </TransitionGroup>

        <div v-if="notifications.length > 5" class="view-all">
          <button @click="viewAll" class="view-all-btn">
            Tümünü Gör ({{ notifications.length }})
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { 
  Bell, BellOff, X, Trash2, CheckCheck, CheckCircle, 
  Info, AlertTriangle, AlertCircle 
} from 'lucide-vue-next'
import { useNotificationStore } from '../stores/notification'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])
const router = useRouter()

const notificationStore = useNotificationStore()
const { notifications, unreadCount } = storeToRefs(notificationStore)

// Show only first 5 notifications
const displayedNotifications = computed(() => {
  return notifications.value.slice(0, 5)
})

const closePanel = () => {
  emit('close')
}

const markAsRead = (id) => {
  notificationStore.markAsRead(id)
}

const markAllAsRead = () => {
  notificationStore.markAllAsRead()
}

const removeNotification = (id) => {
  notificationStore.removeNotification(id)
}

const clearAll = () => {
  if (confirm('Tüm bildirimleri temizlemek istediğinizden emin misiniz?')) {
    notificationStore.clearAll()
  }
}

const viewAll = () => {
  // Navigate to admin dashboard where all notifications are visible
  closePanel()
  router.push({ name: 'AdminDashboard' })
}

const handleNotificationClick = (notification) => {
  // Mark as read
  markAsRead(notification.id)
  
  // Navigate if notification has a route
  if (notification.route) {
    closePanel()
    
    // Handle both string routes and route objects
    if (typeof notification.route === 'string') {
      router.push(notification.route)
    } else {
      router.push(notification.route)
    }
  }
}

const formatTime = (timestamp) => {
  const now = new Date()
  const time = new Date(timestamp)
  const diff = now - time
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Şimdi'
  if (minutes < 60) return `${minutes}dk`
  if (hours < 24) return `${hours}s`
  if (days < 7) return `${days}g`
  
  return time.toLocaleDateString('tr-TR', { 
    day: 'numeric', 
    month: 'short'
  })
}

// Click outside directive
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.notification-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 380px;
  max-height: 500px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
}

/* Header */
.dropdown-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--surface-elevated);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
}

.header-content h3 {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

.unread-badge {
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

/* Notifications List */
.notifications-list {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  color: var(--text-muted);
  text-align: center;
}

.empty-state p {
  font-size: 14px;
  font-weight: 500;
  margin: 12px 0 0;
  color: var(--text-secondary);
}

/* Notification Item */
.notification-item {
  background: var(--surface-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 12px 16px;
  display: flex;
  gap: 10px;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.notification-item.unread {
  background: rgba(99, 102, 241, 0.05);
}

.notification-item.unread::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--indigo-primary);
}

.notification-item:hover {
  background: var(--surface-hover);
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-item.info .notification-icon {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.notification-item.success .notification-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.notification-item.warning .notification-icon {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.notification-item.error .notification-icon {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-content h4 {
  font-size: 13px;
  font-weight: 600;
  margin: 0 0 2px;
  color: var(--text-primary);
}

.notification-content p {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0 0 4px;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notification-time {
  font-size: 10px;
  color: var(--text-muted);
}

.remove-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* View All */
.view-all {
  padding: 12px 16px;
  border-top: 1px solid var(--border-subtle);
  background: var(--surface-elevated);
}

.view-all-btn {
  width: 100%;
  padding: 8px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  color: var(--text-primary);
}

/* Transitions */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.notification-item-enter-active,
.notification-item-leave-active {
  transition: all 0.2s;
}

.notification-item-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.notification-item-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.notification-item-move {
  transition: transform 0.2s;
}

/* Responsive */
@media (max-width: 768px) {
  .notification-dropdown {
    width: calc(100vw - 32px);
    right: 16px;
  }
}

/* Scrollbar */
.notifications-list::-webkit-scrollbar {
  width: 6px;
}

.notifications-list::-webkit-scrollbar-track {
  background: transparent;
}

.notifications-list::-webkit-scrollbar-thumb {
  background: var(--border-subtle);
  border-radius: 3px;
}

.notifications-list::-webkit-scrollbar-thumb:hover {
  background: var(--border-hover);
}
</style>
