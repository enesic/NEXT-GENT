<template>
  <div class="analytics-layout">
    <div class="header">
      <h2>Performans Analizi</h2>
      <div class="date-picker">
        <button class="picker-btn active">Son 30 Gün</button>
        <button class="picker-btn">Bu Yıl</button>
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
import { ref, onMounted, inject } from 'vue'
import LuxuryChart from '../components/LuxuryChart.vue'

const axios = inject('axios')

const conversationData = ref({ series: [], categories: [] })
const conversionData = ref({ series: [], categories: [] })
const statusData = ref({ series: [], labels: [] })

const fetchData = async () => {
    try {
        const convRes = await axios.get('/analytics/daily-conversation-duration')
        conversationData.value = convRes.data
        
        const convRateRes = await axios.get('/analytics/conversion-rate', { 
            params: { start_date: '2026-01-01', end_date: '2026-01-31' } 
        })
        conversionData.value = convRateRes.data

        const statusRes = await axios.get('/analytics/appointment-status-breakdown', { 
            params: { start_date: '2026-01-01', end_date: '2026-01-31' } 
        })
        statusData.value = statusRes.data
        
    } catch (e) {
        console.error("Analytics fetch error:", e)
    }
}

onMounted(fetchData)
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
