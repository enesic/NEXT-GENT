<template>
  <Teleport to="body">
    <div class="toast-container" role="region" aria-label="Notifications" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="notification in visibleNotifications"
          :key="notification.id"
          class="toast"
          :class="[`toast-${notification.type}`, { 'toast-dismissing': notification.dismissing }]"
          role="alert"
          :aria-live="notification.type === 'error' ? 'assertive' : 'polite'"
          @click="dismissNotification(notification.id)"
        >
          <div class="toast-icon">
            <component :is="getIcon(notification.type)" :size="20" :stroke-width="2.5" />
          </div>
          <div class="toast-content">
            <h4 class="toast-title">{{ notification.title }}</h4>
            <p v-if="notification.message" class="toast-message">{{ notification.message }}</p>
          </div>
          <button
            class="toast-close"
            @click.stop="dismissNotification(notification.id)"
            aria-label="Close notification"
          >
            <X :size="18" />
          </button>
          <div
            v-if="notification.type !== 'error' && notification.autoRemove !== false"
            class="toast-progress"
            :style="{ animationDuration: `${notification.duration || 30000}ms` }"
          ></div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { CheckCircle, AlertCircle, AlertTriangle, Info, X } from 'lucide-vue-next'
import { useNotificationStore } from '../../stores/notification'

const notificationStore = useNotificationStore()

// Limit to 5 visible notifications
const visibleNotifications = computed(() => {
  return notificationStore.notifications.slice(0, 5)
})

const getIcon = (type) => {
  const icons = {
    success: CheckCircle,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info
  }
  return icons[type] || Info
}

const dismissNotification = (id) => {
  notificationStore.removeNotification(id)
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
  max-width: 420px;
  width: 100%;
}

.toast {
  pointer-events: auto;
  background: var(--bg-surface);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1),
              0 0 0 1px var(--border-subtle);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;
}

.toast:hover {
  transform: translateX(-4px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.1);
}

.toast-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-success .toast-icon {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.toast-error .toast-icon {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.toast-warning .toast-icon {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.toast-info .toast-icon {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
  line-height: 1.4;
}

.toast-message {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
  word-wrap: break-word;
}

.toast-close {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--surface-hover);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: scale(1.1);
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.4));
  transform-origin: left;
  animation: progress linear forwards;
}

.toast-success .toast-progress {
  background: linear-gradient(90deg, rgba(16, 185, 129, 0.5), #10b981);
}

.toast-error .toast-progress {
  background: linear-gradient(90deg, rgba(239, 68, 68, 0.5), #ef4444);
}

.toast-warning .toast-progress {
  background: linear-gradient(90deg, rgba(245, 158, 11, 0.5), #f59e0b);
}

.toast-info .toast-progress {
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.5), #3b82f6);
}

@keyframes progress {
  from {
    transform: scaleX(1);
  }
  to {
    transform: scaleX(0);
  }
}

/* Toast Transitions */
.toast-enter-active {
  animation: toast-slide-in 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-leave-active {
  animation: toast-slide-out 0.2s cubic-bezier(0.4, 0, 1, 1);
}

@keyframes toast-slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes toast-slide-out {
  from {
    transform: translateX(0) scale(1);
    opacity: 1;
  }
  to {
    transform: translateX(100%) scale(0.9);
    opacity: 0;
  }
}

/* Mobile Responsive */
@media (max-width: 640px) {
  .toast-container {
    top: 16px;
    right: 16px;
    left: 16px;
    max-width: none;
  }

  .toast {
    padding: 14px;
  }

  .toast-icon {
    width: 32px;
    height: 32px;
  }

  .toast-title {
    font-size: 13px;
  }

  .toast-message {
    font-size: 12px;
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .toast-enter-active,
  .toast-leave-active {
    animation-duration: 0.01ms !important;
  }

  .toast {
    transition: none;
  }

  .toast-progress {
    animation: none;
  }
}
</style>
