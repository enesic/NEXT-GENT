<template>
  <div class="analytics-layout">
    <div class="header">
      <h2>Performans Analizi</h2>
      <div class="date-picker">
        <button
          v-for="r in ranges"
          :key="r.label"
          class="picker-btn"
          :class="{ active: selectedRange === r.label }"
          @click="selectRange(r)"
        >{{ r.label }}</button>
      </div>
    </div>

    <div class="charts-grid-analytics">
      <!-- Main Chart 1 -->
      <div class="chart-card large">
        <h3>Günlük Etkileşim Hacmi</h3>
        <LuxuryChart 
          type="area" 
          :series="conversationData.series" 
          :categories="conversationData.categories" 
          height="300" 
        />
      </div>

      <!-- Main Chart 2 -->
      <div class="chart-card">
        <h3> Dönüşüm Oranı</h3>
        <LuxuryChart 
          type="bar" 
          :series="conversionData.series" 
          :categories="conversionData.categories" 
          height="300" 
        />
      </div>

       <!-- Pie Chart -->
       <div class="chart-card">
        <h3> Durum Dağılımı</h3>
        <LuxuryChart 
          type="pie" 
          :series="statusData.series" 
          :labels="statusData.labels" 
          height="300" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LuxuryChart from '../components/LuxuryChart.vue'
import api from '@/config/api'

const conversationData = ref({ series: [], categories: [] })
const conversionData   = ref({ series: [], categories: [] })
const statusData       = ref({ series: [], labels: [] })

const selectedRange = ref('Son 30 Gün')
const ranges = [
  { label: 'Son 30 Gün', days: 30 },
  { label: 'Bu Yıl',     days: 365 },
]

const getDateRange = (days) => {
  const end   = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)
  const fmt = (d) => d.toISOString().split('T')[0]
  return { start_date: fmt(start), end_date: fmt(end) }
}

const fetchData = async (days = 30) => {
  try {
    const convRes = await api.get('/analytics/daily-conversation-duration')
    conversationData.value = convRes.data

    const { start_date, end_date } = getDateRange(days)

    const convRateRes = await api.get('/analytics/conversion-rate', {
      params: { start_date, end_date }
    })
    conversionData.value = convRateRes.data

    const statusRes = await api.get('/analytics/appointment-status-breakdown', {
      params: { start_date, end_date }
    })
    statusData.value = statusRes.data

  } catch (e) {
    console.error('Analytics fetch error:', e)
  }
}

const selectRange = (range) => {
  selectedRange.value = range.label
  fetchData(range.days)
}

onMounted(() => fetchData(30))
</script>

<style scoped>
.analytics-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-picker {
  display: flex;
  gap: 8px;
  background: var(--surface-elevated);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.picker-btn {
  padding: 6px 12px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 6px;
  font-size: 13px;
}

.picker-btn.active {
  background: var(--surface-hover);
  color: var(--text-primary);
  font-weight: 600;
}

.charts-grid-analytics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 24px;
  min-height: 350px;
}

.chart-card.large {
  grid-column: span 2;
}

.chart-card h3 {
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
}

@media (max-width: 1024px) {
  .charts-grid-analytics {
    grid-template-columns: 1fr;
  }
  .chart-card.large {
    grid-column: span 1;
  }
}
</style>
