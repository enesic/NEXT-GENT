<template>
  <div class="sector-dashboard-router">
    <component
      :is="activeSectorComponent"
      :key="sectorStore.currentSectorId || 'default'"
      @navigate="$emit('navigate', $event)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSectorStore } from '../../stores/sector'
import PortalDashboard from '../../views/portal/PortalDashboard.vue'

const sectorStore = useSectorStore()

defineEmits(['navigate'])

// Giriş sonrası Genel Bakış'ta her zaman portal görünsün (Hoş Geldiniz, istatistikler, grafik, hızlı işlemler)
const activeSectorComponent = computed(() => PortalDashboard)
</script>

<style scoped>
.sector-dashboard-router {
  width: 100%;
  min-height: 100%;
}

.dashboard-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
  color: var(--text-secondary);
}

.dashboard-loading p {
  font-size: 14px;
  font-weight: 500;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--current-accent);
  border-radius: 50%;
  animation: sector-spin 0.8s linear infinite;
}

@keyframes sector-spin {
  to { transform: rotate(360deg); }
}
</style>
