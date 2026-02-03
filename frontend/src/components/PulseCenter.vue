<template>
  <Transition name="pulse-slide">
    <div v-if="isVisible" class="pulse-center" :class="{ collapsed: isCollapsed }">
      <!-- Header -->
      <div class="pulse-header" @click="toggleCollapse">
        <div class="pulse-title">
          <Activity :size="16" :stroke-width="2.5" class="pulse-icon" />
          <span>{{ sectorStore.t('dashboard') }} Pulse</span>
        </div>
        <button class="collapse-btn">
          <ChevronDown :size="16" :stroke-width="2" :class="{ rotated: isCollapsed }" />
        </button>
      </div>

      <!-- Metrics Grid -->
      <Transition name="pulse-expand">
        <div v-if="!isCollapsed" class="pulse-metrics">
          <div class="metric-card">
            <div class="metric-icon medical">
              <Phone :size="18" :stroke-width="2" />
            </div>
            <div class="metric-content">
              <div class="metric-label">Aktif {{ sectorStore.t('sessions') }}</div>
              <div class="metric-value">{{ animatedActiveCalls }}</div>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon success">
              <TrendingUp :size="18" :stroke-width="2" />
            </div>
            <div class="metric-content">
              <div class="metric-label">Dönüşüm Oranı</div>
              <div class="metric-value">{{ animatedConversionRate }}%</div>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon info">
              <Users :size="18" :stroke-width="2" />
            </div>
            <div class="metric-content">
              <div class="metric-label">Bugünkü {{ sectorStore.t('clients') }}</div>
              <div class="metric-value">{{ animatedTodayClients }}</div>
            </div>
          </div>

          <div class="metric-card">
            <div class="metric-icon warning">
              <Clock :size="18" :stroke-width="2" />
            </div>
            <div class="metric-content">
              <div class="metric-label">Bekleyen {{ sectorStore.t('appointments') }}</div>
              <div class="metric-value">{{ animatedPendingAppointments }}</div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Live Indicator -->
      <div v-if="!isCollapsed" class="live-indicator">
        <span class="live-dot"></span>
        <span class="live-text">Canlı Veri</span>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, inject } from 'vue'
import { Activity, Phone, TrendingUp, Users, Clock, ChevronDown } from 'lucide-vue-next'
import { useSectorStore } from '../stores/sector'
import gsap from 'gsap'

const sectorStore = useSectorStore()
const axios = inject('axios')

// State
const isVisible = ref(true)
const isCollapsed = ref(false)

// Metrics (simulated real-time data)
const metrics = ref({
  activeCalls: 12,
  conversionRate: 68.5,
  todayClients: 47,
  pendingAppointments: 8
})

// Animated values
const animatedActiveCalls = ref(0)
const animatedConversionRate = ref(0)
const animatedTodayClients = ref(0)
const animatedPendingAppointments = ref(0)

// Methods
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const animateMetric = (target, value) => {
  gsap.to(target, {
    value: value,
    duration: 1.2,
    ease: 'power2.out',
    onUpdate: function() {
      target.value = Math.round(this.targets()[0].value * 10) / 10
    }
  })
}

const updateMetrics = async () => {
  try {
    const response = await axios.get('/analytics/pulse')
    if (response.data) {
      metrics.value = response.data
      
      // Animate to new values
      animateMetric(animatedActiveCalls, metrics.value.activeCalls)
      animateMetric(animatedConversionRate, metrics.value.conversionRate)
      animateMetric(animatedTodayClients, metrics.value.todayClients)
      animateMetric(animatedPendingAppointments, metrics.value.pendingAppointments)
    }
  } catch (error) {
    console.error('Pulse data fetch failed:', error)
  }
}

// Lifecycle
let updateInterval = null

onMounted(() => {
  // Initial fetch
  updateMetrics()
  
  // Update metrics every 10 seconds (optimized for real-time feel vs load)
  updateInterval = setInterval(updateMetrics, 10000)
})

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
})

// Watch for sector changes and refresh
watch(() => sectorStore.currentSector, () => {
  updateMetrics()
})
</script>

<style scoped>
.pulse-center {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 320px;
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6),
              0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  z-index: 100;
  transition: all var(--transition-base);
}

.pulse-center.collapsed {
  width: 240px;
}

.pulse-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-subtle);
  transition: all var(--transition-fast);
}

.pulse-header:hover {
  background: var(--surface-hover);
}

.pulse-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: var(--letter-spacing-normal);
}

.pulse-icon {
  color: var(--current-accent);
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    filter: drop-shadow(0 0 4px var(--current-accent));
  }
  50% {
    filter: drop-shadow(0 0 8px var(--current-accent));
  }
}

.collapse-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.collapse-btn:hover {
  color: var(--text-primary);
}

.collapse-btn svg {
  transition: transform var(--transition-base);
}

.collapse-btn svg.rotated {
  transform: rotate(180deg);
}

.pulse-metrics {
  padding: 16px;
  display: grid;
  gap: 12px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  transition: all var(--transition-fast);
}

.metric-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateX(-2px);
}

.metric-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon.medical {
  background: var(--current-glow);
  color: var(--current-accent);
  box-shadow: 0 0 16px var(--current-glow);
}

.metric-icon.success {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.metric-icon.info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.metric-icon.warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.metric-content {
  flex: 1;
  min-width: 0;
}

.metric-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: var(--letter-spacing-tight);
  color: var(--text-primary);
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid var(--border-subtle);
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 12px #10b981;
  animation: live-pulse 2s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.9);
  }
}

.live-text {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Transitions */
.pulse-slide-enter-active,
.pulse-slide-leave-active {
  transition: all 400ms cubic-bezier(0.4, 0, 0.2, 1);
}

.pulse-slide-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.pulse-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.pulse-expand-enter-active,
.pulse-expand-leave-active {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.pulse-expand-enter-from,
.pulse-expand-leave-to {
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

.pulse-expand-enter-to,
.pulse-expand-leave-from {
  opacity: 1;
  max-height: 500px;
}
</style>
