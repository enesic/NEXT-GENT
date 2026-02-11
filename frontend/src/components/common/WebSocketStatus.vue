<template>
  <div 
    class="ws-status" 
    :class="statusClass" 
    :title="statusText"
    role="status"
    :aria-label="statusText"
  >
    <div class="ws-indicator"></div>
    <span v-if="showLabel" class="ws-label">{{ statusText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useWebSocket } from '../../composables/useWebSocket'

const props = defineProps({
  showLabel: {
    type: Boolean,
    default: false
  }
})

const ws = useWebSocket()

const statusClass = computed(() => {
  if (ws.isConnected.value) return 'ws-connected'
  if (ws.error.value) return 'ws-error'
  return 'ws-connecting'
})

const statusText = computed(() => {
  if (ws.isConnected.value) return 'Canlı'
  if (ws.error.value) return 'Çevrimdışı'
  return 'Bağlanıyor...'
})
</script>

<style scoped>
.ws-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
  transition: all 0.2s;
}

.ws-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ws-label {
  white-space: nowrap;
}

/* Connected state */
.ws-connected {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.ws-connected .ws-indicator {
  background: #10b981;
  animation: pulse 2s ease-in-out infinite;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
}

/* Connecting state */
.ws-connecting {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.ws-connecting .ws-indicator {
  background: #f59e0b;
  animation: blink 1s ease-in-out infinite;
}

/* Error state */
.ws-error {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.ws-error .ws-indicator {
  background: #ef4444;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.2);
  }
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* Hover effect */
.ws-status:hover {
  transform: scale(1.05);
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  .ws-indicator {
    animation: none !important;
  }
  
  .ws-status:hover {
    transform: none;
  }
}

/* Mobile responsive */
@media (max-width: 640px) {
  .ws-status {
    padding: 3px 8px;
    font-size: 10px;
  }
  
  .ws-indicator {
    width: 5px;
    height: 5px;
  }
}
</style>
