<template>
  <div class="offline-notification" v-if="!isOnline">
    <div class="offline-content">
      <WifiOff :size="20" :stroke-width="2" class="offline-icon" />
      <div class="offline-text">
        <span class="offline-title">Bağlantı Kesildi</span>
        <span class="offline-subtitle">İnternet bağlantınızı kontrol edin</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { WifiOff } from 'lucide-vue-next'

const isOnline = ref(navigator.onLine)

const updateOnlineStatus = () => {
  isOnline.value = navigator.onLine
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>

<style scoped>
.offline-notification {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10000;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.offline-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background: rgba(239, 68, 68, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.05);
}

.offline-icon {
  color: white;
  flex-shrink: 0;
}

.offline-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.offline-title {
  font-size: 14px;
  font-weight: 600;
  color: white;
  letter-spacing: var(--letter-spacing-normal);
}

.offline-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  letter-spacing: var(--letter-spacing-normal);
}
</style>
