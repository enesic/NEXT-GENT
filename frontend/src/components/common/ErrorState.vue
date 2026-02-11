<template>
  <div class="error-state" :class="`error-state-${variant}`" role="alert">
    <div class="error-icon" :class="{ 'error-icon-animated': animated }">
      <component :is="getIcon()" :size="iconSize" :stroke-width="2" />
    </div>
    <h3 v-if="title" class="error-title">{{ title }}</h3>
    <p v-if="message" class="error-message">{{ message }}</p>
    <div v-if="$slots.default" class="error-content">
      <slot></slot>
    </div>
    <div v-if="showAction || $slots.action" class="error-actions">
      <slot name="action">
        <button
          v-if="showAction"
          class="btn-error-action"
          @click="handleAction"
          type="button"
        >
          <component v-if="actionIcon" :is="actionIcon" :size="18" />
          <span>{{ actionText }}</span>
        </button>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  WifiOff,
  Database,
  AlertCircle,
  Lock,
  FileQuestion,
  Inbox,
  RefreshCw,
  ArrowLeft,
  Home
} from 'lucide-vue-next'

const props = defineProps({
  variant: {
    type: String,
    default: 'error',
    validator: (value) => ['error', 'network', 'no-data', 'permission', 'not-found', 'empty'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  actionText: {
    type: String,
    default: ''
  },
  actionIcon: {
    type: Object,
    default: null
  },
  showAction: {
    type: Boolean,
    default: true
  },
  iconSize: {
    type: Number,
    default: 48
  },
  animated: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['action'])

const getIcon = () => {
  const icons = {
    error: AlertCircle,
    network: WifiOff,
    'no-data': Database,
    permission: Lock,
    'not-found': FileQuestion,
    empty: Inbox
  }
  return icons[props.variant] || AlertCircle
}

const getDefaultTitle = () => {
  const titles = {
    error: 'Something Went Wrong',
    network: 'Connection Error',
    'no-data': 'No Data Available',
    permission: 'Access Denied',
    'not-found': 'Page Not Found',
    empty: 'No Items Found'
  }
  return props.title || titles[props.variant] || 'Error'
}

const getDefaultMessage = () => {
  const messages = {
    error: 'An unexpected error occurred. Please try again.',
    network: 'Unable to connect to the server. Check your internet connection.',
    'no-data': 'There is no data to display at the moment.',
    permission: 'You do not have permission to access this resource.',
    'not-found': 'The page you are looking for does not exist.',
    empty: 'There are no items to display.'
  }
  return props.message || messages[props.variant] || ''
}

const getDefaultActionText = () => {
  const actions = {
    error: 'Try Again',
    network: 'Retry',
    'no-data': 'Refresh',
    permission: 'Go Back',
    'not-found': 'Go Home',
    empty: 'Add Item'
  }
  return props.actionText || actions[props.variant] || 'Retry'
}

const handleAction = () => {
  emit('action')
}

// Computed values with defaults
const displayTitle = computed(() => getDefaultTitle())
const displayMessage = computed(() => getDefaultMessage())
const displayActionText = computed(() => getDefaultActionText())
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
  min-height: 300px;
}

.error-icon {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  position: relative;
}

.error-icon::before {
  content: '';
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  opacity: 0.2;
}

.error-icon-animated {
  animation: icon-bounce 2s ease-in-out infinite;
}

@keyframes icon-bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Variant styles */
.error-state-error .error-icon {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.error-state-error .error-icon::before {
  background: rgba(239, 68, 68, 0.3);
}

.error-state-network .error-icon {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.error-state-network .error-icon::before {
  background: rgba(245, 158, 11, 0.3);
}

.error-state-no-data .error-icon,
.error-state-empty .error-icon {
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
}

.error-state-no-data .error-icon::before,
.error-state-empty .error-icon::before {
  background: rgba(107, 114, 128, 0.3);
}

.error-state-permission .error-icon {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.error-state-permission .error-icon::before {
  background: rgba(239, 68, 68, 0.3);
}

.error-state-not-found .error-icon {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.error-state-not-found .error-icon::before {
  background: rgba(59, 130, 246, 0.3);
}

.error-title {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}

.error-message {
  font-size: 15px;
  color: #9ca3af;
  line-height: 1.6;
  margin: 0 0 32px 0;
  max-width: 400px;
}

.error-content {
  margin-bottom: 32px;
  color: #d1d5db;
}

.error-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-error-action {
  padding: 12px 24px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-error-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
}

.btn-error-action:active {
  transform: translateY(0);
}

.btn-error-action:focus {
  outline: 2px solid rgba(99, 102, 241, 0.5);
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .error-state {
    padding: 40px 20px;
    min-height: 250px;
  }

  .error-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
  }

  .error-title {
    font-size: 20px;
  }

  .error-message {
    font-size: 14px;
    margin-bottom: 24px;
  }
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .error-icon-animated {
    animation: none;
  }
}
</style>
