<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>Admin Dashboard</h1>
      <p class="subtitle">Sistem performansı ve istatistikler</p>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.label">
        <div class="stat-content">
          <div class="stat-info">
            <p class="stat-label">{{ stat.label }}</p>
            <h2 class="stat-value">{{ stat.value }}</h2>
          </div>
          <span class="stat-change" :class="{ positive: stat.change > 0 }">
            {{ stat.change > 0 ? '+' : '' }}{{ stat.change }}%
          </span>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <!-- Traffic Chart -->
      <div class="chart-card">
        <h3>Trafik Grafiği</h3>
        <div class="chart-container">
          <canvas ref="trafficChart"></canvas>
        </div>
      </div>

      <!-- Flow Chart -->
      <div class="chart-card">
        <h3>Otomasyon Akış Grafiği</h3>
        <div class="chart-container">
          <canvas ref="flowChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Error/Fallback Chart -->
    <div class="chart-card full-width">
      <h3>Hata / Fallback Grafiği</h3>
      <div class="chart-container">
        <canvas ref="errorChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/config/api'

Chart.register(...registerables)

const stats = ref([
  { label: 'Toplam Müşteri', value: '0', change: 0 },
  { label: 'Aylık Gelir', value: '₺0', change: 0 },
  { label: 'Token Tüketimi', value: '0', change: 0 },
  { label: 'Çağrı Sayısı', value: '0', change: 0 }
])

const trafficChart = ref(null)
const flowChart = ref(null)
const errorChart = ref(null)

const trafficData = ref([
  { name: 'Pzt', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Sal', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Çar', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Per', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Cum', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Cmt', calls: 0, whatsapp: 0, automation: 0 },
  { name: 'Paz', calls: 0, whatsapp: 0, automation: 0 }
])

const loadDashboardData = async () => {
  try {
    const response = await api.get('/admin/dashboard')
    const data = response.data
    
    stats.value = [
      { label: 'Toplam Müşteri', value: data.total_customers.toString(), change: data.growth_rate },
      { label: 'Aylık Gelir', value: `₺${data.monthly_revenue.toLocaleString()}`, change: 8 },
      { label: 'Token Tüketimi', value: `${(data.token_consumption / 1000000).toFixed(1)}M`, change: 15 },
      { label: 'Çağrı Sayısı', value: data.total_calls.toLocaleString(), change: 22 }
    ]
  } catch (error) {
    console.error('Dashboard data yüklenemedi:', error)
  }
}

const loadTrafficData = async () => {
  try {
    const response = await api.get('/admin/traffic?days=7')
    trafficData.value = response.data
    renderCharts()
  } catch (error) {
    console.error('Traffic data yüklenemedi:', error)
    renderCharts() // Render with default data
  }
}

const renderCharts = () => {
  // Traffic Chart
  if (trafficChart.value) {
    new Chart(trafficChart.value, {
      type: 'line',
      data: {
        labels: trafficData.value.map(d => d.date),
        datasets: [
          {
            label: 'Çağrılar',
            data: trafficData.value.map(d => d.calls),
            borderColor: '#00D9FF',
            backgroundColor: 'rgba(0, 217, 255, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'WhatsApp',
            data: trafficData.value.map(d => d.whatsapp),
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: 'Otomasyon',
            data: trafficData.value.map(d => d.automation),
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#9ca3af' } }
        },
        scales: {
          y: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          x: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    })
  }

  // Flow Chart (Bar)
  if (flowChart.value) {
    new Chart(flowChart.value, {
      type: 'bar',
      data: {
        labels: ['Hafta 1', 'Hafta 2', 'Hafta 3', 'Hafta 4'],
        datasets: [
          {
            label: 'Başarılı',
            data: [95, 97, 94, 98],
            backgroundColor: '#00D9FF'
          },
          {
            label: 'Fallback',
            data: [5, 3, 6, 2],
            backgroundColor: '#ef4444'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#9ca3af' } }
        },
        scales: {
          y: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          x: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    })
  }

  // Error Chart
  if (errorChart.value) {
    new Chart(errorChart.value, {
      type: 'line',
      data: {
        labels: ['Hafta 1', 'Hafta 2', 'Hafta 3', 'Hafta 4'],
        datasets: [
          {
            label: 'Fallback Oranı (%)',
            data: [5, 3, 6, 2],
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#9ca3af' } }
        },
        scales: {
          y: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          x: { 
            ticks: { color: '#9ca3af' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          }
        }
      }
    })
  }
}

onMounted(() => {
  loadDashboardData()
  loadTrafficData()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: var(--letter-spacing-tight);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: all var(--transition-base);
}

.stat-card:hover {
  background: var(--surface-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: var(--letter-spacing-tight);
}

.stat-change {
  font-size: 14px;
  font-weight: 600;
  color: #ef4444;
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(239, 68, 68, 0.1);
}

.stat-change.positive {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
  position: relative;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
